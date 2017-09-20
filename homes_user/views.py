import hashlib

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect
from django.contrib import messages

from homes_for_sale.models import SaleFavourite, Sale
from homes_to_let.models import LettingFavourite, Letting
from homes.models import Alert


class UserFavouriteView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = "general"

    def __get_sale_favourite(self, slug):
        sale = get_object_or_404(Sale, slug=slug)
        return SaleFavourite.objects.filter(property=sale, user=self.request.user).first()

    def __get_letting_favourite(self, slug):
        letting = get_object_or_404(Letting, slug=slug)
        return LettingFavourite.objects.filter(property=letting, user=self.request.user).first()

    def get(self, request, *args, **kwargs):
        if kwargs['type'] == 'sale':
            favourite = self.__get_sale_favourite(kwargs['slug'])
        else:
            favourite = self.__get_letting_favourite(kwargs['slug'])
        if favourite:
            favourite.delete()
            messages.add_message(request, messages.WARNING, _('You have deleted the selected favourite'))
        return HttpResponseRedirect(reverse('user:dashboard'))


class UserDashboardPageView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = "homes-user-dashboard.html"
    group_required = "general"

    def get_context_data(self, **kwargs):
        context = super(UserDashboardPageView, self).get_context_data(**kwargs)
        context['favourites'] = {
            'sale': SaleFavourite.objects.filter(user=self.request.user),
            'letting': LettingFavourite.objects.filter(user=self.request.user)
        }
        context['alerts'] = Alert.objects.filter(user=self.request.user)
        return context


class UserSubscribeView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = "general"

    def __get_alert_key(self):
        return hashlib.sha1(str(self.__get_request_items())).hexdigest()

    def __get_request_items(self):
        values = {}
        for key, value in self.request.GET.items():
            values[str(key)] = str(value)
        return values

    def __get_or_create_alert(self, key):
        return Alert.objects.get_or_create(
            user=self.request.user,
            key=key,
            defaults={'criteria': self.__get_request_items()}
        )

    def get(self, request, *args, **kwargs):
        obj, created = self.__get_or_create_alert(self.__get_alert_key())
        if created:
            messages.add_message(request, messages.SUCCESS, _('You have subscribed to an email alert for this search'))
        else:
            obj.delete()
            messages.add_message(request, messages.WARNING, _('You were unsubscribed from an email alert for this search'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

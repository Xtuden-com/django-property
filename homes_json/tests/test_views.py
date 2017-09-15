from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.core import serializers

from homes_json.views import SearchPriceView
from homes.factories.search_price_factory import SearchPriceFactory
from homes.models import SearchPrice


class HomesJsonViewsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.search_prices = [
            SearchPriceFactory(type=SearchPrice.SEARCH_PRICE_LETTING),
            SearchPriceFactory(type=SearchPrice.SEARCH_PRICE_SALE)
        ]

    def setup_view(self, view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_view_get_class_method(self):
        prices = serializers.serialize('json', SearchPrice.objects.filter(
            type=SearchPrice.SEARCH_PRICE_LETTING
        ), fields=('label', 'price'))
        request = self.factory.get(reverse('json:search_prices', kwargs={'type':SearchPrice.SEARCH_PRICE_LETTING}))
        view = self.setup_view(SearchPriceView(), request)
        response = view.get(request, SearchPrice.SEARCH_PRICE_LETTING)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content, prices)


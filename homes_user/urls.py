from django.conf.urls import url

from .views import UserDashboardPageView, UserFavouriteView, UserSubscribeView

urlpatterns = [
    url(r'^dashboard/$', UserDashboardPageView.as_view(), name='dashboard'),
    url(r'^favourite/(?P<type>sale|letting)/(?P<slug>[-\w]+)/$', UserFavouriteView.as_view(), name='favourite'),
    url(r'^subscribe/$', UserSubscribeView.as_view(), name='subscribe'),
]

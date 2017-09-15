from django.conf.urls import url

from .views import HomePageView, SearchPageView, DetailPageView, UpdateDistanceView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^search/$', SearchPageView.as_view(), name='search'),
    url(r'^search/details/(?P<slug>[-\w]+)/$', DetailPageView.as_view(), name='detail'),
    url(r'^search/update/$', UpdateDistanceView.as_view(), name='distance')
]

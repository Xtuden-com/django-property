from django.conf.urls import url

from .views import SearchPageView, DetailPageView, UpdateDistanceView

urlpatterns = [
    url(r'^search/$', SearchPageView.as_view(), name='search'),
    url(r'^search/details/(?P<slug>[-\w]+)/$', DetailPageView.as_view(), name='detail'),
    url(r'^search/update/$', UpdateDistanceView.as_view(), name='distance')
]

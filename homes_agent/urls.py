from django.conf.urls import url

from .views import AgentHomePageView, AgentBranchHomePageView

urlpatterns = [
    url(r'^$', AgentHomePageView.as_view(), name='home'),
    url(r'^branch/(?P<slug>[-\w]+)/$', AgentBranchHomePageView.as_view(), name='branch')
]

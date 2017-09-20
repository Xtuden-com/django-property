from django.conf.urls import url

from .views import AgentBranchHomePageView

urlpatterns = [
    url(r'^branch/(?P<slug>[-\w]+)/$', AgentBranchHomePageView.as_view(), name='branch')
]

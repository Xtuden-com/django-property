from django.conf.urls import url

from .views import AgentHomePageView

urlpatterns = [
    url(r'^$', AgentHomePageView.as_view(), name='home'),
]

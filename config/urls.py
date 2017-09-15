from django.conf.urls import url, include
from django.contrib import admin

from homes.views import HomePageView, CustomRegistrationView

admin.site.site_header = 'Django Property'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sales/', include('homes_for_sale.urls', namespace='sales')),
    url(r'^lettings/', include('homes_to_let.urls', namespace='lettings')),
    url(r'^user/', include('homes_user.urls', namespace='user')),
    url(r'^agents/', include('homes_agent.urls', namespace='agents')),
    url(r'^accounts/register/$', CustomRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^json/', include('homes_json.urls', namespace='json')),
    url(r'^$', HomePageView.as_view(), name='homepage')
]

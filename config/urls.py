from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from homes.views import HomePageView, CustomRegistrationView
from homes.forms import CustomAuthenticationForm

admin.site.site_header = 'Django Property'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sales/', include('homes_for_sale.urls', namespace='sales')),
    url(r'^lettings/', include('homes_to_let.urls', namespace='lettings')),
    url(r'^user/', include('homes_user.urls', namespace='user')),
    url(r'^agents/', include('homes_agent.urls', namespace='agents')),
    url(r'^accounts/login/$', auth_views.login, {'authentication_form': CustomAuthenticationForm}, name='login'),
    url(r'^accounts/register/$', CustomRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^json/', include('homes_json.urls', namespace='json')),
    url(r'^$', HomePageView.as_view(), name='homepage')
]

from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^password/update/$', views.update_password, name='update_password'),
    url(r'^password/forgot/$', views.forgot_password, name='forgot_password'),
    url(r'^password/forgot/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.forgot_password_confirm, name='forgot_password_confirm'),
    url(r'^auth/token/$', views.GetJSONWebToken.as_view(), name='auth_token'),
]

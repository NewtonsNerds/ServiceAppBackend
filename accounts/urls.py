from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<pk>[0-9]+)/', views.detail, name='detail'),
    url(r'^password/reset/', views.reset_password, name='reset_password'),
    url(r'^auth/token/', views.GetJSONWebToken.as_view(), name='auth_token'),
]
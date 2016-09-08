from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^auth/token/', views.GetJSONWebToken.as_view(), name='auth_token'),
]
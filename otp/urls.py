from django.conf.urls import url
from django.contrib import admin

from .views import(
	get_otp,
	verify_otp,
	)

urlpatterns = [
    url(r'^$', get_otp),
    url(r'^verify_otp/$', verify_otp),
    #url(r'^posts/$', <appname>.views.<funcname>),
]
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$', views.register_user, name='register'),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.user_confirm,
        name='confirm'),
    url(r'^resend/$', views.resend_confirmation, name='resend'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout')
]
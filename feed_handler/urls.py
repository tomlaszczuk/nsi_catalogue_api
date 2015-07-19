from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageTemplateView.as_view(), name='home-page'),
    url(r'^update/$', views.ManualFeedUpdateView.as_view(), name='update')
]
from django.conf.urls import patterns, url

from hunter import views

urlpatterns = patterns('',
    url(r'^$', views.CalcView, name='calc'),
    # ex: /hunter/5/
)
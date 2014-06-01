from django.conf.urls import patterns, url

from hunter import views

urlpatterns = patterns('',
    url(r'^$', views.CalcView, name='calc'),
    url(r'^armory_process', views.ArmoryProcessForm, name='armory_process'),
    url(r'^(?P<region>\w+)/(?P<server>\w+)/(?P<character>\w+)', views.ArmoryView, name='armory'),
    # ex: /hunter/5/
)
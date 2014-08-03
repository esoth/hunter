from django.conf.urls import patterns, url

from hunter import views

urlpatterns = patterns('',
    url(r'^$', views.CalcView, name='calc'),
    url(r'^model', views.ModelView, name='model'),
    url(r'^aoemodel', views.ModelAoEView, name='aoemodel'),
    url(r'^debug_model', views.ModelDebugView, name='modeldebug'),
    url(r'^scaling', views.ScalingView, name='scale'),
    url(r'^scalestat', views.ScaleStatView, name='scalestat'),
    url(r'^armory_process', views.ArmoryProcessForm, name='armory_process'),
    url(r'^(?P<region>\w+)/(?P<server>\w+)/(?P<character>\w+)/(?P<spec>\w+)', views.ArmoryView, name='armory'),
    url(r'^(?P<region>\w+)/(?P<server>\w+)/(?P<character>\w+)', views.ArmoryView, name='armory'),
    # ex: /hunter/5/
)
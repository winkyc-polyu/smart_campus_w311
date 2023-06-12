from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('onoff', views.publish_on_off, name='onoff'),
    path('', views.index, name='index'),
]
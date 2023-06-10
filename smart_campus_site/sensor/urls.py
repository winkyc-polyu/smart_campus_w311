from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('temp_data', views.temp_data, name='temp_data'),
    path('temp_info', views.temp_info),
    path('hum_info', views.hum_info),
    path('light_info', views.light_info),
    path('snd_info', views.snd_info),
]
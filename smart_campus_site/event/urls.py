from django.urls import path
from . import views

urlpatterns = [

path('list', views.list),
path('test', views.form_input),
]
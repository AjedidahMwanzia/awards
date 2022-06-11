from django.urls import path, re_path as url
from . import views


urlpatterns = [
    path('',views.home ,name= 'home'),
   
]
from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('link', link, name='link'),
    path('<str:slug>', find),
    
]

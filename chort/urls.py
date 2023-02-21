from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('link', link, name='link'),
    path('qr/codes',  QRcodes, name='qr_codes'),
    path('links',  links, name='links'),
    path('custom/links',  customLinks, name='custom_links'),
    path('settings',  settings, name='settings'),
    path('contact',  contact, name='contact'),
    path('chart/country', countryChart, name="country_chart"),






    
    path('<str:slug>', find),
    
    
]

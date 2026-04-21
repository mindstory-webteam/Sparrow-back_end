# ventures/urls.py
from django.urls import path
from . import views

app_name = 'ventures'

urlpatterns = [
    path('', views.sector_list, name='home'),
    path('sectors/', views.sector_list, name='sector_list'),
    path('sector/<slug:slug>/', views.sector_detail, name='sector_detail'),
    path('<slug:sector_slug>/<slug:venture_slug>/', views.venture_detail, name='venture_detail'),
]
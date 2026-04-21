
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.about, name='about'),
    # path('automotive/', views.automotive, name='automotive'),
    # path('shell-lubricants/', views.shell_lubricants, name='shell_lubricants'),
    # path('two-three-wheeler/', views.two_three_wheeler, name='two_three_wheeler'),
    # path('it-technology/', views.it_technology, name='it_technology'),
    path('career/', views.career, name='career'),
    path('contact/', views.contact, name='contact'),
    path('test-404/', views.test_404),  # ← Visit this to see your 404 page
]
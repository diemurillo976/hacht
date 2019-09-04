from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('dashboard_pacientes/', views.dashboard_pacientes, name='dashboard_pacientes')
]


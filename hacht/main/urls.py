from django.urls import path
from . import views
from django.urls import path, include # new

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    #path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('dashboard_pacientes/', views.dashboard_pacientes, name='dashboard_pacientes'),
    path('dashboard_sesiones/', views.dashboard_sesiones, name='dashboard_sesiones'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('features/', views.features, name='features')
]


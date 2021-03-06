from django.urls import path
from . import views
from .Analytics import Paciente, Sesion
from django.urls import path, include # new

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')), #Agrega pantalla de login
    path('login_app/', views.login_app, name="login_app"), #Engloba logins para implementaciones de clientes
    path('registration/', views.registration, name='registration'),
    path('dashboard_pacientes/', views.dashboard_pacientes, name='dashboard_pacientes'),
    path('dashboard_sesiones/', views.dashboard_sesiones, name='dashboard_sesiones'),
    path('contact_us/', views.contact_us, name='contact_us'), #El formulario html de contacto existe pero no está implementada su funcionalidad
    path('features/', views.features, name='features'),
    path('demo/', views.demo, name='demo'),
    path('demo_app/', views.demo, name='demo_cliente_movil'),
    path('dashboard_pacientes/components/descriptivo_paciente/', views.descriptivo_paciente, name="descriptivo_paciente"),
    path('dashboard_sesiones/components/descriptivo_sesion/', views.descriptivo_sesion, name="descriptivo_sesion"),
    path('dashboard_pacientes/eliminar/', views.eliminar_paciente, name="eliminar_paciente"),
    path('dashboard_sesiones/eliminar/', views.eliminar_sesion, name="eliminar_sesion"),
    path('dashboard_sesiones/components/muestras_sesion/', views.muestras_sesion, name="muestras_sesion"),
    path('dashboard_sesiones/agregar_muestra/', views.agregar_muestra, name="agregar_muestra"),
    path('dashboard_sesiones/modificar_muestra/', views.modificar_muestra, name="modificar_muestra"),
    path('dashboard_sesiones/components/analytics_sesion/', Sesion.analytics_sesion, name="analytics_sesion"),
    path('demo/components/comp_demo/', views.demo, name='comp_demo'),
    path('dashboard_pacientes/components/analytics_paciente/', Paciente.analytics_paciente, name="analytics_paciente"),
    path('about_us/', views.about_us, name="about_us"),
    path('help/', views.ayuda, name="help")
]

# Gets new handler for the specific 500 error
handler500 = views.handle_500_error

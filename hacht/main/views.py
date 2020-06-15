
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver
from django.template.defaulttags import register
from django.utils.safestring import mark_safe


from .Clients import ClientFactory


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    print(credentials)
    print("Login fallado para las credenciales: {}".format(credentials))

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    print(user)
    print("Se loggeó correctamente el usuario {}".format(user))

#Los siguientes métodos determinan el comportamiento de la aplicación
#al establecer las respuestas que dará el server a las peticiones a Los
#sitios de urls.py
#Con tal de permitir un comportamiento deistinto según el tipo de cliente
#que haga un request, se utiliza un patrón factory, con métodos con ducktyping
#Las implementaciones concretas de estos comportamientos están en la carpeta Clients/Implementations

#método para mostrar la página de "sobre nosotros"
def about_us(request):
    client = ClientFactory.get_client(request)

    return client.about_us(request)

#método para mostrar la página de "ayuda"
def ayuda(request):

    client = ClientFactory.get_client(request)

    return client.ayuda(request)


# Funcion to handle error responses
def handle_error(request, status, message):

    client = ClientFactory.get_client(request)

    return client.handle_error(request, status, message)

# Function to catch the 500 internal error
def handle_500_error(request):

    return handle_error(request, status=500, message="El servidor ha tenido un problema resolviendo la petición")


#Método para mostrar la página de inicio de la aplicación
def index(request):

    client = ClientFactory.get_client(request)

    return client.index(request)

#Método para realizar proceso de login en clientes distintos al web;
#para el cliente web este método funciona para redirigir al usuario después de loggears
def login_app(request):
    client = ClientFactory.get_client(request)

    return client.login_app(request)


#Método para el manejo del registro de usuarios
def registration(request):
    client = ClientFactory.get_client(request)

    return client.registration(request)


#Método para mostrar mensajes de éxito al registrarse
def registration_success(request):
    client = ClientFactory.get_client(request)

    return client.registration_success(request)

#Método que se encarga del funcionamiento del demo de la aplicación según el tipo de cliente
def demo(request):

    client = ClientFactory.get_client(request)
    return client.demo(request)


#Método para el manejo de la información de los pacientes asociados a un médico
def dashboard_pacientes(request):
    client = ClientFactory.get_client(request)

    return client.dashboard_pacientes(request)


#Método específico para mostrar los datos de un paciente
def descriptivo_paciente(request):

    client = ClientFactory.get_client(request)

    return client.descriptivo_paciente(request)

#Método para eliminar un paciente relacionado a un médico
def eliminar_paciente(request):

    client = ClientFactory.get_client(request)

    return client.eliminar_paciente(request)

#Método para el manejo de la información de las sesiones asociadas a un paciente o a un investigador
def dashboard_sesiones(request):

    client = ClientFactory.get_client(request)

    return client.dashboard_sesiones(request)

#Método específico para mostrar los datos de una sesión
def descriptivo_sesion(request):

    client = ClientFactory.get_client(request)

    return client.descriptivo_sesion(request)

#Método para eliminar una sesión relacionada a un paciente o a un investigador
def eliminar_sesion(request):

    client = ClientFactory.get_client(request)

    return client.eliminar_sesion(request)

#Método para obtener las muestras relacionadas a una sesión
def muestras_sesion(request):

    client = ClientFactory.get_client(request)

    return client.muestras_sesion(request)

#Método para agregar una nueva muestra a una sesión
def agregar_muestra(request):

    client = ClientFactory.get_client(request)

    return client.agregar_muestra(request)

#Método para modificar las muestras asociadas a una sesión
def modificar_muestra(request):

    client = ClientFactory.get_client(request)

    return client.modificar_muestra(request)

#Método para mostrar la información de contacto
def contact_us(request):
    client = ClientFactory.get_client(request)

    return client.contact_us(request)

#Método para mostrar la información de funcionalidades disponibles en la aplicación
def features(request):
    client = ClientFactory.get_client(request)

    return client.features(request)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))

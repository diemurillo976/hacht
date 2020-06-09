import sys
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, Paciente, Sesion
from .forms import RegistrationForm, Data_PacienteN, Data_Comp_Sesion_Completo, Muestra, Data_Sesion_Muestra
from django.http import HttpResponse
from django.db.models import Model, Count
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.contrib.auth import authenticate, login
from django.dispatch import receiver
from django.db.models.query import QuerySet
from django.template.defaulttags import register
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
import numpy as np
import os
from django.conf import settings



from .Clients import ClientFactory

#model imports#################################################

from PIL import Image
from io import BytesIO
import requests


from .CNN_src.forward import *


############################################################################

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    print(credentials)
    print("Login fallado para las credenciales: {}".format(credentials))

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    print(user)
    print("Se loggeó correctamente el usuario {}".format(user))



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



def index(request):
    client = ClientFactory.get_client(request)

    return client.index(request)


def login_app(request):
    client = ClientFactory.get_client(request)

    return client.login_app(request)


def registration(request):
    client = ClientFactory.get_client(request)

    return client.registration(request)


def registration_success(request):
    client = ClientFactory.get_client(request)

    return client.registration_success(request)

def demo(request):
    client = ClientFactory.get_client(request)

    return client.demo(request)


def dashboard_pacientes(request):
    client = ClientFactory.get_client(request)

    return client.dashboard_pacientes(request)



def descriptivo_paciente(request):

    client = ClientFactory.get_client(request)

    return client.descriptivo_paciente(request)


def eliminar_paciente(request):

    client = ClientFactory.get_client(request)

    return client.eliminar_paciente(request)


def dashboard_sesiones(request):

    client = ClientFactory.get_client(request)

    return client.dashboard_sesiones(request)


def descriptivo_sesion(request):

    client = ClientFactory.get_client(request)

    return client.descriptivo_sesion(request)

def eliminar_sesion(request):

    client = ClientFactory.get_client(request)

    return client.eliminar_sesion(request)

def muestras_sesion(request):

    client = ClientFactory.get_client(request)

    return client.muestras_sesion(request)

def agregar_muestra(request):

    client = ClientFactory.get_client(request)

    return client.agregar_muestra(request)


def demo_app_muestra(request):

    client = ClientFactory.get_client(request)

    return client.demo_app_muestra(request)


def modificar_muestra(request):

    client = ClientFactory.get_client(request)

    return client.modificar_muestra(request)


def contact_us(request):
    client = ClientFactory.get_client(request)

    return client.contact_us(request)

def features(request):
    client = ClientFactory.get_client(request)

    return client.features(request)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))

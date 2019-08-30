from django.shortcuts import render


def index(request):
    return render(request, 'index/index.html')

def login(request):
    return render(request, 'index/login.html')


def registration(request):
    return render(request, 'index/registration.html')

def dashboard_pacientes(request):
    return render(request, 'index/dashboard_pacientes.html')

def dashboard_sesiones(request):
    return render(request, 'index/dashboard_sesiones.html')
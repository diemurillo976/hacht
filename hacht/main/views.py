import sys
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, Paciente, Sesion
from .forms import RegistrationForm, Data_PacienteN, Data_Comp_Sesion_Completo, Muestra, Data_Sesion_Muestra
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.db.models import Model, Count
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.contrib.auth import authenticate, login
from django.dispatch import receiver
from django.db.models.query import QuerySet
from django.template.defaulttags import register
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
import random
import json
import numpy as np
import os
import csv
import time
from datetime import datetime

#Pyrebase and model imports#################################################
import pyrebase
from PIL import Image
from io import BytesIO
import requests

#Comentado por motivos de falta de espacio en el hosting
#sys.path.insert(0,'/home/Martinvc96/hacht/hacht/main/CNN_src/')
#sys.path.insert(0,'C:/Users/gmc_2/source/repos/HACHT/hacht/hacht/main/CNN_src/')

# Define el path a CNN_src y lo agrega al sys.path
path = os.getcwd()
path = os.path.join(path, "hacht", "main", "CNN_src")
#path = os.path.join(path, "main", "CNN_src")
print(path)
sys.path.insert(0, path)
from .CNN_src.forward import *

#Firebase auth##############################################################

config = {
    "apiKey": "AIzaSyArQxRet5XqKI6v8948A2ZnHZOZsu7vCNY",
    "authDomain": "hacht-7d98d.firebaseapp.com",
    "databaseURL": "https://hacht-7d98d.firebaseio.com",
    "projectId": "hacht-7d98d",
    "storageBucket": "hacht-7d98d.appspot.com",
    "messagingSenderId": "225406534324",
    "appId": "1:225406534324:web:f5317f74d07ced54"
  }

#Firebase Storage reference#

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

############################################################################

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    print(credentials)
    print("Login fallado para las credenciales: {}".format(credentials))

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    print(user)
    print("Se loggeó correctamente el usuario {}".format(user))

# Auxiliar function to return a list of static images and their corresponding class
def read_static_list():

    # Obtiene el path del archivo csv con la lista
    path = os.getcwd()
    abs_path = os.path.join(path, "hacht", "main", "static", "index", "assets", "csv", "demo_src.csv")

    with open(abs_path) as file:

        reader = csv.reader(file, delimiter=',')
        lista = []

        for row in reader:

            y_true, url = row[0], row[1]
            lista.append((y_true, url))

    return lista

def ayuda(request):

    if request.user.is_authenticated:

        context = {"logged_in" : True}
        return render(request, 'index/help.html', context)

    return render(request, 'index/help.html')

# Funcion to handle error responses
def handle_error(request, status, message):

    # send error to android client
    if request.GET.get("android") or request.POST.get("android"):
        response = HttpResponse(json.dumps({'message': message}), 
            content_type='application/json')
        response.status_code = status
        return response

    # render a error message page
    else:
        
        # This needs to be changed
        return HttpResponse(status=status)

# Function to catch the 500 internal error 
def handle_500_error(request):

    return handle_error(request, status=500, message="El servidor ha tenido un problema resolviendo la petición")    

# Function to handle each response to the android client
# It serializes the data on the context variable
def get_for_android(request, context=None):

    token = get_token(request)

    if context is not None:

        # Itera sobre todo el contexto, cuando hay querysets los convierta a listas para poder serializar
        try:

            for key in context:
                if isinstance(context[key], QuerySet):
                    context[key] = list(context[key].values())
                elif isinstance(context[key], Model):
                    context[key] = model_to_dict(context[key])

            context["token"] = token
            print("Contexto en get_for_android: {}".format(context))

            try:
                return JsonResponse(context, safe=False)
            except Exception as e:
                print("Error respondiendo al request: {}".format(str(e)))
                return HttpResponse(status=500)

        except Exception as e:

            print("Error casteando objetos del context: {}.".format(str(e)))
            return HttpResponse(status=500)

    else:

        return JsonResponse({'token' : token})

def index(request):

    if request.GET.get("android"):
        return get_for_android(request)
    else:
        return render(request, 'index/index.html')

def login_app(request):

    if(request.method == 'POST'):

        if request.user.is_authenticated:
            context = {
                    'exito' : 'true'
                }
            return get_for_android(request, context)

        else:

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                context = {
                    'exito' : 'true'
                }
                return get_for_android(request, context)

    else:

        return handle_error(
            request, 
            status=400, 
            message="La petición está formada de manera incorrecta, debe enviar un formulario \"POST\" para que el servidor le pueda dar respuesta."
            )

def registration(request):

    if(request.method == 'POST'):
        
        form = RegistrationForm(request.POST)

        if(form.is_valid()):

            # Creates the django's user
            new_user = User(username=request.POST['correo'],
                            email=request.POST['correo'],
                            first_name=request.POST['nombre'])

            new_user.set_password(request.POST['password'])
            new_user.save()

            new_user.profile.rol = request.POST["rol"]
            new_user.profile.org = request.POST["org"]

            new_user.save()
            print('NUEVO REGISTRO USER AGREGADO')
            #messages.success(request, _('El usuario ha sido creado con éxito'))

            return redirect('registration_success')

        else:

            return handle_error(
                request,
                status=400,
                message="No se podido completar la adición del usuario, por favor revise los datos ingresados y que estos sean válidos"
            )

    if(request.method == 'GET'):
        form = RegistrationForm()

    context = {'form' : form}
    return render(request, 'index/registration.html', context)


def registration_success(request):
    return render(request, 'index/registration_success.html')

def demo(request):

    if request.method == "GET" and request.GET.get("resultado"):

        lista = read_static_list()

        index = int(request.GET["index"])
        y_true, url = lista[index]
        resultado = int(request.GET["resultado"])
        estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

        context = {"class": y_true,
                   "url": url,
                   "resultado": estimations[resultado],
                   "index": index}

        return render(request, 'index/components/comp_demo.html', context)

    elif request.method == "GET" and request.GET.get("index"):

        lista = read_static_list()

        index = int(request.GET["index"])
        y_true, url = lista[index]
        context = {"class": y_true,
                   "url": url,
                   "index": index}

        return render(request, 'index/components/comp_demo.html', context)

    elif request.method == "GET":

        return render(request, 'index/demo.html')

    elif request.method == "POST":

        time.sleep(1)

        index = int(request.POST["index"])
        url = request.POST["url"]

        url_fire = storage.child(url)
        response = requests.get(url)

        img = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        result = forward_single_img(img_cv)

        context = {
            "index" : index,
            "resultado" : result
        }

        return render(request, "index/demo.html", context)


def dashboard_pacientes(request):

    # Only the medic user should be seeing "patients"
    if request.user.is_authenticated and request.user.profile.rol == '0':

        if request.method == "GET":

            all_patients_n = Paciente.objects.filter(id_user=request.user)
            context = {'pacientes': all_patients_n}

            if request.GET.get("android"):
                return get_for_android(request, context)
            else:
                return render(request, 'index/dashboard_pacientes.html', context)

        elif request.method == "POST":

            if request.POST.get("id"):

                id_p = request.POST["id"]
                instancia_paciente = get_object_or_404(Paciente, pk=id_p)
                form = Data_PacienteN(request.POST, instance=instancia_paciente)

            else:

                form = Data_PacienteN(request.POST)

            if(form.is_valid()):

                paciente = form.save()
                paciente.id_user = request.user
                paciente.save()

                return redirect('/dashboard_pacientes/')

            else:

                return handle_error(
                    request,
                    status=400,
                    message="No se ha podido agregar el paciente. Se encontraron los errores: \n{}".format(str(form._errors))
                )
    
    # If the user is authenticated and is a medic, gets redirected to dashboard_sesiones
    elif request.user.is_authenticated:

        if request.GET.get("android"):
            return redirect('/dashboard_sesiones/?android=1', permanent=True)
        else:
            return redirect('dashboard_sesiones', permanent=True)

    else:
        
        return handle_error(
            request,
            status=401,
            message="El usuario no está autenticado, para acceder a esta funcionalidad primero debe ingresar con sus credenciales"
        )

def descriptivo_paciente(request):

    # Si no hay paciente seleccionado se envía el form vacio
    if request.GET.get("id_paciente"):

        id_p = int(request.GET["id_paciente"])

        # Obtiene el paciente
        paciente = Paciente.objects.get(pk=id_p)

        # Crea el formulario
        form = Data_PacienteN(instance=paciente)

    else:

        # Crea el formulario
        form = Data_PacienteN()

    context = {'form': form}
    return render(request, 'index/components/descriptivo_paciente.html', context)

def eliminar_paciente(request):

    if request.POST.get("id_paciente"):

        id_p = request.POST["id_paciente"]
        paciente = Paciente.objects.get(pk=id_p)
        paciente.delete()
        return HttpResponse(status=204) # Se procesó correctamente pero no hay contenido

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def dashboard_sesiones(request):

    if request.user.is_authenticated:
        
        # Si hay un id_paciente en el get entonces el método debería haber sido llamado 
        # por un usuario médico. Dentro se chequea que el paciente perteneza al usuario
        if request.method == "GET" and request.GET.get("id_paciente") and request.user.profile.rol == '0':

            paciente = Paciente.objects.get(pk=request.GET["id_paciente"])

            # Evita que con la dirección correcta se obtenga el valor
            if paciente.id_user != request.user:
                return HttpResponse(status=403)

            sesiones = Sesion.objects.filter(id_paciente=request.GET["id_paciente"])
            context = {"paciente" : paciente, "sesiones" : sesiones}

            if request.GET.get("android"):

                return get_for_android(request, context)

            else:

                return render(request, 'index/dashboard_sesiones.html', context)

        # Cuando es usuario investigador
        elif request.method == "GET":

            sesiones = Sesion.objects.filter(id_usuario=request.user.id)
            context = {'sesiones' : sesiones}
            
            if request.GET.get("android"):

                return get_for_android(request, context)

            else:

                return render(request, 'index/dashboard_sesiones.html', context)

        elif request.method == "POST":

            if request.POST.get("id"):

                # Obtiene los datos ingresados contra los dato
                id_s = request.POST["id"]
                instancia_sesion = get_object_or_404(Sesion, pk=id_s)
                form = Data_Comp_Sesion_Completo(request.POST, instance=instancia_sesion)

            else:

                # Popula el formulario solo con los datos obtenidos del post
                form = Data_Comp_Sesion_Completo(request.POST)

            if(form.is_valid()):

                sesion = form.save()

                if request.user.profile.rol == '0':
                    id_paciente = request.POST["id_paciente"]
                    sesion.id_paciente = id_paciente
                    sesion = form.save()
                    return redirect('/dashboard_sesiones/?id_paciente=' + id_paciente)
                else:
                    id_usuario = request.user.id
                    sesion.id_usuario = id_usuario
                    sesion = form.save()
                    return redirect('/dashboard_sesiones/')

            else:
                print(str(form._errors))


            return render(request, 'index/dashboard_sesiones.html')

        else:
            return HttpResponse(status=404)

    else:
        return HttpResponse(status=403)


def descriptivo_sesion(request):

    if request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)
        form = Data_Comp_Sesion_Completo(instance=sesion)

    else:

        form = Data_Comp_Sesion_Completo()

    if request.GET.get("id_paciente"):

        id_paciente = request.GET["id_paciente"]
        context = {'form': form, 'id_paciente': id_paciente}

    else:
        context = {'form': form}

    return render(request, 'index/components/descriptivo_sesion.html', context)

def eliminar_sesion(request):

    if request.POST.get("id_sesion"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)
        sesion.delete()
        return HttpResponse(status=204) # Se procesó correctamente pero no hay contenido

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def muestras_sesion(request):

    if request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        if request.GET.get("android"):

            muestras = Muestra.objects.filter(sesion=id_s)
            context = {
                'sesion' : sesion,
                'muestras' : muestras
            }

            return get_for_android(request, context)

        else:

            muestras = []

            for muestra in Muestra.objects.filter(sesion=id_s):
                form = Data_Sesion_Muestra(instance=muestra)
                muestras.append(form)


            context = {
                'sesion' : sesion,
                'forms' : muestras
            }

            return render(request, 'index/components/muestras_sesion.html', context)

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def agregar_muestra(request):

    if request.POST.get("id_sesion"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        # Obtiene los múltiples archivos
        files = request.FILES.getlist('img_file')

        # Por cada archivo lo sube a Firebase, hace la predicción y lo agrega a la BD local
        for file in files:
            
            steps = 0
            exito = False
            guardada = False

            while steps < 5 and not exito:

                try:
                    
                    if guardada == False:
                        storage.child(str(file)).put(file)
                        guardada = True

                    url = storage.child(str(file)).get_url(None)
                    response = requests.get(url)

                    img = Image.open(BytesIO(response.content))
                    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    result = forward_single_img(img_cv)
                    estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

                    muestra = Muestra(
                        sesion=sesion,
                        url_img=url,
                        pred=estimations[result],
                    )

                    muestra.save()

                    exito = True

                except:
                    steps += 1

            if not exito:
                return handle_error(request, status=500, message="Lo sentimos, no se ha podido establecer la conexión con la base de datos para imágenes. Al menos en alguna muestra se han realizado más de 5 intentos para establecer la conexión.")

        if request.user.profile.rol == '0':
            return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido
        else:
            return redirect('/dashboard_sesiones/') # Se procesó correctamente pero no hay contenido

    else:
        # Maneja el error de que no llegue id_sesion
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def demo_app_muestra(request):

    if request.GET.get("android") and request.GET.get("url"):

        url = request.GET["url"]
        response = requests.get(url)

        img = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        result = forward_single_img(img_cv)
        estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

        context = {
                'estimacion' : estimations[result]
            }

        return get_for_android(request, context)

    else:
        return HttpResponse(status=403)


def modificar_muestra(request):

    if request.POST.get("id_muestra") and request.POST.get("update"):

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        if request.POST.get("consent"):
            muestra.consent = request.POST["consent"]
        if request.POST.get("pred_true"):
            muestra.pred_true = request.POST["pred_true"]

        muestra.obs = request.POST["obs"]

        muestra.save()

        if request.user.profile.rol == '0':
            return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido
        else:
            return redirect('/dashboard_sesiones/')

    elif request.POST.get("id_muestra") and request.POST.get("delete"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        muestra.delete()

        return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente))

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

# Auxiliar function to assist the analytics for Sesion
# It gets metrics associated with each class present
def get_metrics(muestras_general):

    # Obtains the "Muestra" objects grouping by "pred" and counting it
    muestras_pred = muestras_general.values('pred').annotate(
        cantidad=Count('pred'))

    # Group by pred_true adding the count of it
    muestras_pred_true = muestras_general.values('pred_true').annotate(
        cantidad=Count('id'))

    muestras_val = muestras_general.values('pred', 'pred_true')

    # Flatten the results
    muestras_p = muestras_pred.values_list('pred', flat=True)
    muestras_pt = muestras_pred_true.values_list('pred_true', flat=True)

    # Gets unique values
    possible_values = list(muestras_p) + list(muestras_pt)
    possible_values = list(dict.fromkeys(possible_values))

    # We have to check if None is a possibility; it makes sense in the model, not in here
    if None in possible_values:
        possible_values.remove(None)

    metrics_dict = {}
        
    for value in possible_values:

        TP = muestras_val.filter(pred=value, pred_true=value).count()
        FP = muestras_val.filter(pred=value).exclude(pred_true=value).count()
        FN = muestras_val.filter(pred_true=value).exclude(pred=value).count()
        TN = muestras_val.exclude(pred_true=value).exclude(pred=value).count()

        precission = 0

        if (TP + FP) != 0:
            precission = TP / (TP + FP)

        recall = 0

        if (TP + FN) != 0:
            recall = TP / (TP + FN)

        specificity = 0

        if (TN + FN) != 0:
            specificity = TN / (TN + FN)

        f1_score = 0

        if (precission + recall) != 0:
            f1_score = 2 * ((precission * recall) / (precission + recall))

        val_dict = {
            'TP' : TP,
            'FP' : FP,
            'FN' : FN,
            'TN' : TN,
            'precission' : precission,
            'recall' : recall,
            'specificity' : specificity,
            'f1_score' : f1_score
        }

        metrics_dict[value] = val_dict

    return metrics_dict, possible_values

def analytics_sesion(request):

    def random_color():

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return 'rgba({}, {}, {}, 255)'.format(r, g, b)

    if request.method == "GET" and request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]

        muestras_general = Muestra.objects.filter(sesion=id_s)

        muestras_no_val = muestras_general.values('pred_true').filter(pred_true=None).annotate(
            cantidad=Count("id")
        )

        try:
            cantidad_no_val = muestras_no_val.values_list("cantidad", flat=True).get(pred_true=None)
        except:
            cantidad_no_val = 0

        datos_muestras = muestras_general.values('pred').annotate(
            cantidad=Count('pred'),
            probabilidad=Count('pred') / Count('id')).order_by('-cantidad')

        data = []
        labels = []
        colors = []

        for dato in datos_muestras:
            data.append(dato['cantidad'])
            labels.append(dato['pred'])
            colors.append(random_color())

        data_obj = {

            'datasets' : [{
                'data' : data,
                'backgroundColor' : colors
            }],

            'labels' : labels,

        }

        data_obj = json.dumps(data_obj)

        val_dict, possible_values = get_metrics(muestras_general)

        context = {
            'datos_muestras' : datos_muestras,
            'data' : data_obj,
            'val_dict' : val_dict,
            'classes' : possible_values,
            'cantidad_no_val' : cantidad_no_val
        }

        if request.GET.get("android"):
            return render(request, 'index/components/sesion_graficos_app.html', context)
        else:
            return render(request, 'index/components/sesion_graficos.html', context)

def analytics_paciente(request):

    def random_color():

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return 'rgba({}, {}, {}, 255)'.format(r, g, b)

    if request.method == "GET":

        # Gets all "Muestra" objects with its related "Sesion" object
        datos_muestras = Muestra.objects.select_related('sesion').all()

        # Obtains all "Muestra" objects grouped by "pred" field of sesion
        datos_muestras = datos_muestras.values(
            'sesion_id', 'sesion__date', 'pred', 'sesion__id_paciente', 'sesion__id_usuario').annotate(
                cantidad=Count('pred'),
                probabilidad=Count('pred') / Count('id'))

        # Orders the set by cantidad in a descending manner
        datos_muestras = datos_muestras.order_by('-cantidad')

        # Filters the query to only those important to the session at hand
        if request.user.profile.rol == '0':
            id_p = request.GET["id_paciente"]
            datos_muestras = datos_muestras.filter(sesion__id_paciente=id_p)
        else:
            id_u = request.user.id
            datos_muestras = datos_muestras.filter(sesion__id_usuario=id_u)

        # Gets the possible values of "pred" according to Muestra objects
        # As distinct() is not working, we get the predictions and dates and then filter to get only the unique ones
        possible_predictions = datos_muestras.values_list("pred", flat="true").order_by("pred")
        possible_predictions = list(dict.fromkeys(possible_predictions))

        possible_dates = datos_muestras.values_list("sesion__date", flat="true").order_by("sesion__date")
        possible_dates = list(dict.fromkeys(possible_dates))

        datasets = []
        labels_datasets = []

        for prediction in possible_predictions:

            fechas_vistas = []

            if prediction not in labels_datasets:

                data = []

                for date in possible_dates:
                    
                    # These will be the x axis of the plot
                    if str(date) not in labels_datasets:
                        labels_datasets.append(str(date))

                    if str(date) not in fechas_vistas:
                        
                        try:
                            
                            # This is the y axis
                            dato = datos_muestras.get(sesion__date=date, pred=prediction)
                            data.append(dato["cantidad"])

                        except Exception as e:
                            
                            # If the record does not exist then it must be 0
                            data.append(0)

                        fechas_vistas.append(str(date))
                
                color = random_color()
                        
                dataset = {
                    'data' : data,
                    'label' : prediction,
                    'backgroundColor': color,
                    'borderColor': color,
                    'fill': False
                }

                datasets.append(dataset)

        data_obj = {
            'datasets' : datasets,
            'labels' : labels_datasets
        }

        data_obj = json.dumps(data_obj)

        """
        Obtiene un resumen de los datos para graficar en tipo pie
        Esto significa que obtiene las muestras y lo único que importa es la cantidad de cada tipo
        de tumor existente en la base para el paciente.
        """

        datos_muestras = Muestra.objects.select_related('sesion').all()
        datos_muestras = datos_muestras.values('pred', 'sesion__id_paciente').annotate(
                cantidad=Count('pred'),
                probabilidad=Count('pred') / Count('id'))
        datos_muestras = datos_muestras.order_by('-cantidad')
        datos_muestras = datos_muestras.filter(sesion__id_paciente=id_p)

        data = []
        labels = []
        colors = []

        for dato in datos_muestras:
            data.append(dato['cantidad'])
            labels.append(dato['pred'])
            colors.append(random_color())

        data_pie_obj = {

            'datasets' : [{
                'data' : data,
                'backgroundColor' : colors
            }],

            'labels' : labels,

        }

        data_pie_obj = json.dumps(data_pie_obj)

        context = {
            'datos_muestras' : datos_muestras,
            'data_line' : data_obj,
            'data_pie' : data_pie_obj
        }

        if request.GET.get("android"):
            return render(request, 'index/components/paciente_graficos_app.html', context)
        else:
            return render(request, 'index/components/paciente_graficos.html', context)

def contact_us(request):
    return render(request, 'index/contact-us.html')

def features(request):
    return render(request, 'index/features.html' )

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))
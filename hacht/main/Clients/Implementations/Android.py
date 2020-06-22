from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from ...models import User, Profile, Paciente, Sesion
from ...forms import Data_PacienteN, Data_Comp_Sesion_Completo, Muestra
from django.contrib.auth import authenticate, login
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from PIL import Image
from io import BytesIO
import requests
import json
from ...CNN_src import TumourClasses

class android_client:
    def __init__(self):
        self.name = "android"

    def handle_error(self, request, status, message):

        # send error to android client
        response = HttpResponse(json.dumps({'message': message}),
            content_type='application/json')
        response.status_code = status
        return response

    def index(self, request):
        return self.__get_for_android(request)

    def login_app(self, request):

        if(request.method == 'POST'):

            if request.user.is_authenticated:
                context = {
                        'exito' : 'true'
                    }
                return self.__get_for_android(request, context)

            else:

                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    context = {
                        'exito' : 'true'
                    }
                    return self.__get_for_android(request, context)

        else:

            return self.handle_error(
                request,
                status=400,
                message="La petición está formada de manera incorrecta, debe enviar un formulario \"POST\" para que el servidor le pueda dar respuesta."
                )

    #la funcionalidad para registration no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def registration(self, request):
        return self.index(request)

    #la funcionalidad para registration_success no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def registration_success(self, request):
        return self.index(request)

    #Para el cliente móvil, el demo consiste en cargar una imagen y recibir una predicción
    def demo(self, request):
        if request.GET.get("url"):

            url = request.GET["url"]
            response = requests.get(url)

            img = Image.open(BytesIO(response.content))
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            result, probabilities = forward_single_img(img_cv)
            
            probabilities = list(probabilities[0,:].tolist())
            probabilities = [(TumourClasses.estimation_labels[i], probabilities[i]) for i in range(0, len(TumourClasses.estimation_labels))]


            context = {
                    'estimacion' : TumourClasses.estimation_labels[result]
                }

            return __get_for_android(request, context)

        else:
            return HttpResponse(status=403)


    #Solo está implementada la muestra de la información de los pacientes
    def dashboard_pacientes(self, request):
        # Only the medic user should be seeing "patients"
        if request.user.is_authenticated and request.user.profile.rol == '0':

            if request.method == "GET":

                all_patients_n = Paciente.objects.filter(id_user=request.user)
                context = {'pacientes': all_patients_n}

                return __get_for_android(request, context)


        else:

            return self.handle_error(
                request,
                status=401,
                message="El usuario no está autenticado, para acceder a esta funcionalidad primero debe ingresar con sus credenciales"
            )


    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def descriptivo_paciente(self, request):
        return self.index(request)

    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def eliminar_paciente(self, request):
        return self.index(request)

    #Solo está implementada la muestra de la información de las sesiones
    def dashboard_sesiones(self, request):

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

                return __get_for_android(request, context)


            # Cuando es usuario investigador
            elif request.method == "GET":

                sesiones = Sesion.objects.filter(id_usuario=request.user.id)
                context = {'sesiones' : sesiones}

                return __get_for_android(request, context)

        else:
            return HttpResponse(status=403)

    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def descriptivo_sesion(self, request):

        return self.index(request)

    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def eliminar_sesion(self, request):
        return self.index(request)


    #La información de las muestras se devuelve serializada en un json
    def muestras_sesion(self, request):

        if request.GET.get("id_sesion"):

            id_s = request.GET["id_sesion"]
            sesion = Sesion.objects.get(pk=id_s)

            muestras = Muestra.objects.filter(sesion=id_s)
            context = {
                'sesion' : sesion,
                'muestras' : muestras
            }

            return __get_for_android(request, context)


        else:

            # Maneja el error de que no llegue id_paciente
            print("El request llegó vacio")
            return HttpResponse(status=400) # Problema con el request




    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def agregar_muestra(self, request):
        return self.index(request)


    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def modificar_muestra(self, request):
        return self.index(request)

    def ayuda(self, request):

        if request.user.is_authenticated:

            context = {"logged_in" : True}
            return render(request, 'index/help.html', context)

        return render(request, 'index/help.html')

    def contact_us(self, request):
        return render(request, 'index/contact-us.html')

    def features(self, request):
        return render(request, 'index/features.html' )

    #Método para mostrar los gráficos de los objetos de analytics del paciente
    def show_graficos_paciente(self, request, context):
        return render(request, 'index/components/paciente_graficos_app.html', context)

    #Método para mostrar los gráficos de los objetos de analytics de la sesión
    def show_graficos_sesion(self, request, context):
        return render(request, 'index/components/sesion_graficos_app.html', context)

    # Function to handle each response to the android client
    # It serializes the data on the context variable
    def __get_for_android(self, request, context=None):

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

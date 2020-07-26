from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ...models import User, Profile, Paciente, Sesion
from ...forms import RegistrationForm, Data_PacienteN, Data_Comp_Sesion_Completo, Muestra, Data_Sesion_Muestra, ContactUsForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
import json
import csv
import os
import time
from PIL import Image
from io import BytesIO
import numpy as np
import requests
from ...CNN_src.forward import *
from ...CNN_src import TumourClasses
from ...Analytics import Sorters

class web_client:
    def __init__(self):
        self.name = "web"

    def handle_error(self, request, status, message):

        # render a error message page
        # This needs to be changed
        context = {'message': message}
        #return HttpResponse(status=status, content=message)
        return render(request, 'index/error.html', context, status=status)

    def index(self, request):
        return render(request, 'index/index.html')

    def about_us(self, request):
        return render(request, 'index/about_us.html')


    def login_app(self, request):
        if request.user.is_authenticated:
            if request.user.profile.rol == '0':
                return redirect('dashboard_pacientes')
            else:
                return redirect('dashboard_sesiones')

    #TODO no se guarda el input 'uso' en la BD.
    def registration(self, request):
        if(not request.user.is_authenticated):
            if(request.method == 'POST'):

                form = RegistrationForm(request.POST)

                if(form.is_valid()):

                    if(User.objects.filter(email=request.POST['correo'])):
                        messages.error(request, 'Ya existe una cuenta asociada a este correo')
                        return render(request, 'index/registration.html', {'form' : RegistrationForm()})

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

                    user = authenticate(username=new_user.username, password=request.POST['password'])
                    login(request, user)

                    return render(request, 'index/registration.html')

                else:

                    return self.handle_error(
                        request,
                        status=400,
                        message="No se podido completar la adición del usuario, por favor revise los datos ingresados y que estos sean válidos"
                    )

            if(request.method == 'GET'):
                form = RegistrationForm()

            context = {'form' : form}

            return render(request, 'index/registration.html', context)

        else:
            return self.handle_error(
                request,
                status = 400,
                message="Acceso no autorizado a pagina."
            )



    #Para la aplicación web el demo se basa en mostrar imágenes a las que se les puede
    #consultar sus predicciones con sus categorías.
    def demo(self, request):

        context = {}

        # Load url of demo images to the context
        images = []
        for element in self.__read_static_list():
            url = element[1]
            images += [url]

        matrix = []
        for i in range(0, len(images), 4):
            r = []
            for j in range(0, 4):
                r.append((images[i + j], i + j))
            matrix.append(r)

        if request.method == "GET" and request.GET.get("resultado"):
        # Calcula el nuevo resultado de la imagen.

            lista = self.__read_static_list()

            index = int(request.GET["index"])
            y_true, url = lista[index]
            resultado = int(request.GET["resultado"])


            context_aux = {"class": y_true,
                           "url": url,
                           "resultado": TumourClasses.estimation_labels[resultado],
                           "index": index,
                           "images": matrix}

            context.update(context_aux)
            return render(request, 'index/components/comp_demo.html', context)

        elif request.method == "GET" and request.GET.get("index"):
            # Devuelve la imagen seleccionada.
            lista = self.__read_static_list()

            index = int(request.GET["index"])
            y_true, url = lista[index]
            context_aux = {"class": y_true,
                           "url": url,
                           "index": index}
            context.update(context_aux)
            return render(request, 'index/components/comp_demo.html', context)

        elif request.method == "GET":
            # Carga demo.html por primera vez.

            context_aux = {
                "images" : matrix
            }
            context.update(context_aux)
            return render(request, 'index/demo.html', context)

        elif request.method == "POST":

            #time.sleep(1)

            index = int(request.POST["index"])
            url = request.POST["url"]

            #url_fire = settings.FIREBASE_STORAGE.child(url)
            response = requests.get(url)

            img = Image.open(BytesIO(response.content))
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            result, probabilities = forward_single_img(img_cv)

            probabilities = list(probabilities[0,:].tolist())
            probabilities = [(TumourClasses.estimation_labels[i], probabilities[i]) for i in range(0, len(TumourClasses.estimation_labels))]
            print("Probabilidades de clase predichas:")
            print(probabilities)


            context_aux = {
                "index" : index,
                "resultado" : result,
                "images": matrix
            }
            context.update(context_aux)

            return render(request, "index/demo.html", context)


    #Se muestra información y se maneja la creación y edición de pacientes
    def dashboard_pacientes(self, request):
        # Only the medic user should be seeing "patients"
        if request.user.is_authenticated and request.user.profile.rol == '0':

            if request.method == "GET":

                all_patients_n = Paciente.objects.filter(id_user=request.user)

                #Ordena los pacientes para mostrar primero aquellos con predicciones malignas en la última sesión
                all_patients_n = sorted(all_patients_n, key=Sorters.pacientes_sort_key, reverse=True)

                context = {'pacientes': all_patients_n}
                context.update({"logged_in" : "usr_doctor"})
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

                    return self.handle_error(
                        request,
                        status=400,
                        message="No se ha podido agregar el paciente. Se encontraron los errores: \n{}".format(str(form._errors))
                    )

        # If the user is authenticated and is a medic, gets redirected to dashboard_sesiones
        elif request.user.is_authenticated:
            return self.handle_error(
                request,
                status=401,
                message="El usuario no tiene permiso de acceder a esta funcionalidad."
            )
        else:

            return self.handle_error(
                request,
                status=401,
                message="El usuario no está autenticado, para acceder a esta funcionalidad primero debe ingresar con sus credenciales."
            )

    #Método utilizado para el manejo de los forms del html en los que se muestra, edita y crea a los pacientes
    #Se usa en conjunto con dashboard_pacientes
    def descriptivo_paciente(self, request):

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


    def eliminar_paciente(self, request):

        if request.POST.get("id_paciente"):

            id_p = request.POST["id_paciente"]
            paciente = Paciente.objects.get(pk=id_p)
            paciente.delete()
            # Se procesó correctamente pero no hay contenido
            return self.handle_error(
                request,
                status=204,
                message="Ha ocurrido un problema realizando la acción."
            )

        else:

            # Maneja el error de que no llegue id_paciente
            print("El request llegó vacio")

            # Problema con el request
            return self.handle_error(
                request,
                status=400,
                message="Ha ocurrido un problema realizando la acción."
            )


    #Se muestra información y se maneja la creación y edición de sesiones,
    #ya sea relacionadas a un paciente o a un investigador
    def dashboard_sesiones(self, request):

        if request.user.is_authenticated:

            # Si hay un id_paciente en el get entonces el método debería haber sido llamado
            # por un usuario médico. Dentro se chequea que el paciente perteneza al usuario
            if request.method == "GET" and request.GET.get("id_paciente") and request.user.profile.rol == '0':

                paciente = Paciente.objects.get(pk=request.GET["id_paciente"])

                # Evita que con la dirección correcta se obtenga el valor
                if paciente.id_user != request.user:
                    return self.handle_error(
                        request,
                        status=403,
                        message="Ha ocurrido un problema realizando la acción."
                    )

                sesiones = Sesion.objects.filter(id_paciente=request.GET["id_paciente"]).order_by("-date")

                context = {"paciente" : paciente, "sesiones" : sesiones}
                context.update({"logged_in" : "usr_doctor"})
                return render(request, 'index/dashboard_sesiones.html', context)

            # Cuando es usuario investigador
            elif request.method == "GET":

                sesiones = Sesion.objects.filter(id_usuario=request.user.id).order_by("-date")
                context = {'sesiones' : sesiones}
                context.update({"logged_in" : "usr_investigador"})

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
                return self.handle_error(
                    request,
                    status=404,
                    message="Ha ocurrido un problema realizando la acción."
                )

        else:
            return self.handle_error(
                request,
                status=401,
                message="El usuario no está autenticado, para acceder a esta funcionalidad primero debe ingresar con sus credenciales."
            )

    #Método utilizado para el manejo de los forms del html en los que se muestra, edita y crea a las sesiones
    #Se usa en conjunto con dashboard_sesiones
    def descriptivo_sesion(self, request):

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

    def eliminar_sesion(self, request):

        if request.POST.get("id_sesion"):

            id_s = request.POST["id_sesion"]
            sesion = Sesion.objects.get(pk=id_s)
            sesion.delete()
            # Se procesó correctamente pero no hay contenido
            return self.handle_error(
                request,
                status=204,
                message="Ha ocurrido un problema realizando la acción."
            )

        else:

            # Maneja el error de que no llegue id_paciente
            print("El request llegó vacio")

            # Problema con el request
            return self.handle_error(
                request,
                status=400,
                message="Ha ocurrido un problema realizando la acción."
            )
  
    #Las muestras se usan para cargar el componente de html respectivo
    def muestras_sesion(self, request):

        if request.GET.get("id_sesion"):

            id_s = request.GET["id_sesion"]
            sesion = Sesion.objects.get(pk=id_s)

            muestras = []

            for muestra in Muestra.objects.filter(sesion=id_s):
                form = Data_Sesion_Muestra(instance=muestra)
                muestras.append(form)


            #Ordena las muestras para mostrar primero aquellas con predicciones malignas
            muestras = sorted(muestras, key=Sorters.muestras_sort_key, reverse=True)

            context = {
                'sesion' : sesion,
                'forms' : muestras
            }

            return render(request, 'index/components/muestras_sesion.html', context)

        else:

            # Maneja el error de que no llegue id_paciente
            print("El request llegó vacio")

            # Problema con el request
            return self.handle_error(
                request,
                status=400,
                message="Ha ocurrido un problema realizando la acción."
            )

    #Se agrega la muestra y se le adjunta la predicción correspondiente, para volver a cargar
    #la vista de muestras actualizada
    def agregar_muestra(self, request):

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
                            settings.FIREBASE_STORAGE.child(str(file)).put(file)
                            guardada = True

                        url = settings.FIREBASE_STORAGE.child(str(file)).get_url(None)
                        response = requests.get(url)

                        img = Image.open(BytesIO(response.content))
                        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                        result, probabilities = forward_single_img(img_cv)

                        probabilities = list(probabilities[0,:].tolist())
                        probabilities = [(TumourClasses.estimation_labels[i], probabilities[i]) for i in range(0, len(TumourClasses.estimation_labels))]
                        print("Probabilidades de clase predichas:")
                        print(probabilities)

                        muestra = Muestra(
                            sesion=sesion,
                            url_img=url,
                            pred=TumourClasses.estimation_labels[result],
                        )

                        muestra.save()

                        exito = True

                    except:
                        steps += 1

                if not exito:
                    return self.handle_error(request, status=500, message="Lo sentimos, no se ha podido establecer la conexión con la base de datos para imágenes. Al menos en alguna muestra se han realizado más de 5 intentos para establecer la conexión.")

            if request.user.profile.rol == '0':
                return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido
            else:
                return redirect('/dashboard_sesiones/') # Se procesó correctamente pero no hay contenido

        else:
            # Maneja el error de que no llegue id_sesion
            print("El request llegó vacio")
            # Problema con el request
            return self.handle_error(
                request,
                status=400,
                message="Ha ocurrido un problema realizando la acción."
            )


    #Se actualiza la información de una muestra o se borra de la base de datos
    #Pero no se elimina la foto del repositorio de imágenes
    def modificar_muestra(self, request):

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
            # Problema con el request
            return self.handle_error(
                request,
                status=400,
                message="Ha ocurrido un problema realizando la acción."
            )


    def ayuda(self, request):
        return render(request, 'index/help.html')

    #TODO este metodo lee el mensaje pero nunca es guardado en la BD.
    def contact_us(self, request):

        if request.method == "GET":

            form = ContactUsForm()
            context = {'form' : form}
            return render(request, 'index/contact-us.html', context)

        elif request.method == "POST":
            form = ContactUsForm(request.POST)

            if(form.is_valid()):
                nombre = request.POST["nombre"]
                asunto = request.POST["asunto"]
                email = request.POST["email"]
                mensaje = request.POST["mensaje"]


                return redirect('contact_us')

        else:
            return self.handle_error(
                request,
                status=404,
                message="Ha ocurrido un problema realizando la acción."
            )


    def features(self, request):
        return render(request, 'index/features.html')



    #Método para mostrar los gráficos de los objetos de analytics del paciente
    def show_graficos_paciente(self, request, context):
        return render(request, 'index/components/paciente_graficos.html', context)

    #Método para mostrar los gráficos de los objetos de analytics de la sesión
    def show_graficos_sesion(self, request, context):
        return render(request, 'index/components/sesion_graficos.html', context)

    # Auxiliar function to return a list of static images and their corresponding class
    def __read_static_list(self):

        # Obtiene el path del archivo csv con la lista
        path = settings.STATIC_ROOT
        abs_path = os.path.join(path, "index", "assets", "csv", "demo_src.csv")

        with open(abs_path) as file:

            reader = csv.reader(file, delimiter=',')
            lista = []

            for row in reader:

                y_true, url = row[0], row[1]
                lista.append((y_true, url))

        return lista

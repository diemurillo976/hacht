from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import User
from ...forms import RegistrationForm
from django.conf import settings
from django.contrib import messages
import json
import csv
import os
import time
from PIL import Image
from io import BytesIO
import requests
from ...CNN_src.forward import *


class web_client:
    def __init__(self):
        self.name = "web"

    def handle_error(self, request, status, message):

        # render a error message page
        # This needs to be changed
        return HttpResponse(status=status, content=message)

    def index(self, request):
        return render(request, 'index/index.html')

    #Implementación cubierta por django para el cliente web_client
    #Se mantiene este método dummy para fines de uniformidad con el
    #patrón de diseño
    #Se redirige a login
    def login_app(self, request):
        return redirect('login')

    def registration(self, request):
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

    def registration_success(self, request):
        return render(request, 'index/registration_success.html')

    def demo(self, request):
        if request.method == "GET" and request.GET.get("resultado"):

            lista = self.__read_static_list()

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

            lista = self.__read_static_list()

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

            url_fire = settings.FIREBASE_STORAGE.child(url)
            response = requests.get(url)

            img = Image.open(BytesIO(response.content))
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            result = forward_single_img(img_cv)

            context = {
                "index" : index,
                "resultado" : result
            }

            return render(request, "index/demo.html", context)


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

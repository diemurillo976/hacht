from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
import json

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

    #la funcionalidad para demo no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def demo(self, request):
        return self.index(request)


    def dashboard_pacientes(self, request):
        # Only the medic user should be seeing "patients"
        if request.user.is_authenticated and request.user.profile.rol == '0':

            if request.method == "GET":

                all_patients_n = Paciente.objects.filter(id_user=request.user)
                context = {'pacientes': all_patients_n}

                return __get_for_android(request, context)


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

            return redirect('/dashboard_sesiones/?android=1', permanent=True)

        else:

            return handle_error(
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

    #la funcionalidad  no está implementada en cliente android
    #Pero se mantiene este método para uniformidad del patrón de diseño
    #Se redirige a método index
    def eliminar_sesion(self, request):
        return self.index(request)


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


    def demo_app_muestra(self, request):

        if request.GET.get("url"):

            url = request.GET["url"]
            response = requests.get(url)

            img = Image.open(BytesIO(response.content))
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            result = forward_single_img(img_cv)
            estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

            context = {
                    'estimacion' : estimations[result]
                }

            return __get_for_android(request, context)

        else:
            return HttpResponse(status=403)

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

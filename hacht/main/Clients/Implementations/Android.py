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

from .Implementations import *

#Diccionario para guardar funciones que instancian cada una de las implementaciones
#de los clientes. Utilizada en ClientFactory. Las implementaciones se cargan
#del paquete Implementations
clients = {"web": lambda  : Web.web_client(),
            "android": lambda  : Android.android_client()}

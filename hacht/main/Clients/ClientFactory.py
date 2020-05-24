from .Client_list import clients

def get_client(request):
    #if request.GET.get("android"):
    #Cambiar peticiones url para implementar cliente mediante el parametro "client", en vez de "android=1"
    for client in clients:
        if (request.GET.get(client) or request.POST.get(client)):
            return clients[client]()
    return clients["web"]()

from .Client_list import clients

def get_client(request):
    #if request.GET.get("android"):
    #Cambiar peticiones url para implementar cliente mediante el parametro "client", en vez de "android=1"
    for client in clients:
        if (request.GET.get(client.key)):
            return client.value()
        return clients["web"]()

def dummy(request):
    #if request.GET.get("android"):
    #Cambiar peticiones url para implementar cliente mediante el parametro "client", en vez de "android=1"
    for client in clients:
        if (request.GET.get(client.key)):
            cliente = client.value
            print(cliente.name)
        if (client.key == "web"):
            cliente = client.value
            print(cliente.name)

def hola():
    for client in clients:
        print(client)
        cliente = clients[client]()
        print(cliente.name)

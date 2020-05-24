from django.http import HttpResponse
from django.shortcuts import render
import json


class web_client:
    def __init__(self):
        self.name = "web"

    def handle_error(self, request, status, message):

        # render a error message page
        # This needs to be changed
        return HttpResponse(status=status)

    def index(self, request):
        return render(request, 'index/index.html')

    #Se redirige a login
    def login_app(self, request):
        return redirect('login')

from django.contrib import admin

from .models import Profile, Paciente, Sesion, Muestra

admin.site.register(Profile)
admin.site.register(Paciente)
admin.site.register(Sesion)
admin.site.register(Muestra)


# Register your models here.

from django.contrib import admin

from .models import Profile, Paciente_N, Paciente_A, Sesion, Muestra

admin.site.register(Profile)
admin.site.register(Paciente_N)
admin.site.register(Paciente_A)
admin.site.register(Sesion)
admin.site.register(Muestra)


# Register your models here.

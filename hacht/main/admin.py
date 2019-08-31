from django.contrib import admin

from .models import User, Paciente_N, Paciente_A, Sesion, Muestra

admin.site.register(User)
admin.site.register(Paciente_N)
admin.site.register(Paciente_A)
admin.site.register(Sesion)
admin.site.register(Muestra)


# Register your models here.

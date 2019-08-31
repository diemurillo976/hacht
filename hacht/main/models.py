from __future__ import unicode_literals
from djongo import models


## User object definition
class User(models.Model):
    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    nombre = models.CharField(max_length=40, null=True)
    correo = models.EmailField(max_length=40, null=True)
    password = models.CharField(max_length=100, null=True)
    salt = models.CharField(max_length=100, null=True)
    org = models.CharField(max_length=100, null=True)
    rol = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.nombre


## Paciente_N object definition
class Paciente_N(models.Model):
    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    id_user = models.PositiveIntegerField(null=True)
    nombre = models.EmailField(max_length=40, null=True)
    ced = models.CharField(max_length=10, null=True)
    sexo = models.CharField(max_length=1, null=True)
    edad = models.PositiveSmallIntegerField(null=True)
    res = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre



## Paciente_A object definition
class Paciente_A(models.Model):
    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    id_user = models.PositiveIntegerField(null=True)
    identificador = models.EmailField(max_length=40, null=True)
    sexo = models.CharField(max_length=1, null=True)
    edad = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.identificador


## Sesion object definition
class Sesion(models.Model):
    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    id_paciente = models.PositiveIntegerField(null=True)
    date = models.DateField()
    obs = models.CharField(max_length=500, null=True)
    estado = models.CharField(max_length = 1, null=True)

    def __str__(self):
        return self.id_paciente


## Muestra object definition
class Muestra(models.Model):
    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    id_sesion = models.PositiveIntegerField(null=True)
    url_img = models.URLField(null=True)
    pred = models.CharField(max_length=8, null=True)
    accuracy = models.FloatField(null=True)
    obs = models.CharField(max_length=200, null=True)
    is_true = models.CharField(max_length=1, null=True)
    consent = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.id_sesion
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


## Profile object definition
## Extends the "default" User model; using a one to one field and linking it with the User
class Profile(models.Model):

    # one to one relationship with the django auth default user
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                primary_key=True,
                                default=1) # Default value should exit on "auth_user" table

    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    # attributes that make our "user" different than the django's
    org = models.CharField(max_length=100, null=True)
    rol = models.CharField(max_length=1, null=True)

def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Method that catches the "save User event" and automatically saves the changes made to a profile
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  

post_save.connect(create_user, sender=User)
post_save.connect(save_profile, sender=User)
#post_save.connect(save_profile, sender=User)
        
## Paciente_N object definition
class Paciente_N(models.Model):
    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    id_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1) # Default value should exit on "auth_user" table)
    nombre = models.CharField(max_length=40, null=True)
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

    id_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1) # Default value should exit on "auth_user" table)
    identificador = models.CharField(max_length=40, null=True)
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

    # Ojo que para usar una sola llave foranea necesitamos generalizar Paciente!
    id_paciente = models.PositiveIntegerField(null=True)
    date = models.DateField()
    obs = models.CharField(max_length=500, null=True, blank=True)
    estado = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.id_paciente


## Muestra object definition
class Muestra(models.Model):

    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    #id_sesion = models.IntegerField(null=True)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, default=-1)
    url_img = models.URLField(null=True)
    pred = models.CharField(max_length=20, null=True)
    accuracy = models.FloatField(null=True)
    obs = models.CharField(max_length=200, null=True, blank=True)
    is_true = models.BooleanField(max_length=1, null=True)
    consent = models.BooleanField(max_length=1, null=True)

    def __str__(self):
        return self.id_sesion
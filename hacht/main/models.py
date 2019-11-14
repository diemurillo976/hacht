from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

## Profile object definition
## Extends the "default" User model; using a one to one field and linking it with the User
class Profile(models.Model):
    """
    Entidad 'Perfil' creada con la intención de unificar las entidades 'Médico' e 'Investigador' y manejar los atributos 'organización' y 'rol' de las entidades.
    """

    # one to one relationship with the django auth default user
    #user = models.IntegerField()
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
        
## Paciente_N object definition
class Paciente(models.Model):
    """
    Entidad que modela al 'Paciente'. Atributos: Id, nombre, cédula, sexo, edad, residencia.
    """

    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    #id_user = models.IntegerField(null=True)
    id_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1) # Default value should exist on "auth_user" table)
    nombre = models.CharField(max_length=40, null=True)
    ced = models.CharField(max_length=10, null=True)
    sexo = models.CharField(max_length=1, null=True)
    edad = models.PositiveSmallIntegerField(null=True)
    res = models.CharField(max_length=50, null=True)

    ## As the model for Sesion doesnt have explicit FKs to Paciente
    ## We need to force the On Delete - Cascade behaviour
    def delete(self, **kwargs):
        """ 
        Entrada: id del objeto paciente a eliminar
        Salida: Ninguna
        Descripción: Elimina al paciente dado su id del modelo en la base de datos.
        """

        # Gets the pacient id
        paciente_id = self.id

        # For each sesion associated with the pacient id; we delete each sesion instance
        for sesion in Sesion.objects.filter(id_paciente=paciente_id):
            sesion.delete()

        # Now the object can be deleted safely
        super(Paciente, self).delete()

    def __str__(self):
        """ 
        Entrada: Objeto de tipo 'Paciente' 
        Salida: String 'nombre'
        Descripción: Función que retorna el nombre del paciente
        """
        return self.nombre


## Sesion object definition
class Sesion(models.Model):
    """
    Entidad que modela la 'Sesión'. Atributos: Id de paciente, Id de usuario,  fecha, observación, estado.
    """

    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    id_paciente = models.PositiveIntegerField(null=True)
    id_usuario = models.PositiveIntegerField(null=True) # para UI de investigador
    date = models.DateField()
    obs = models.CharField(max_length=500, null=True, blank=True)
    estado = models.CharField(max_length=1, null=True)

    def __str__(self):
        """ 
        Entrada: Objeto de tipo 'Sesión' 
        Salida: String 'Id del paciente'
        Descripción: Función que retorna el id de paciente de una sesión dada.
        """
        return self.id_paciente


## Muestra object definition
class Muestra(models.Model):
    """
    Entidad que modela la 'Muestra'. Atributos: Id de sesión, url de la imagen,  predicción, observación, Validación de la predicción, consentimiento de uso.
    """

    #auto update on new data
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    #auto update on data change
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    #sesion = models.IntegerField(null=True)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, default=-1)
    url_img = models.URLField(null=True)
    pred = models.CharField(max_length=20, null=True)
    obs = models.CharField(max_length=200, null=True, blank=True)
    pred_true = models.CharField(max_length=20, null=True, blank=True)
    consent = models.BooleanField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.id_sesion

# Creates callbacks to add and update the profile of a user when the user has been created or updated
def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Method that catches the "save User event" and automatically saves the changes made to a profile
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  

# Creates the callback so that whenever a muestra is deleted; then the image associated is too
def delete_muestra_callback(sender, instance, **kwargs):

    url = instance.url_img
    ## does something with url to delete from firebase

def delete_user_callback(sender, instance, **kwargs):

    # We emulate the cascade effect
    for sesion in Sesion.objects.filter(id_usuario=instance.id):
        sesion.delete()

# Connect the callbacks to the signal they should be listening to
post_save.connect(create_user, sender=User)
post_save.connect(save_profile, sender=User)

post_delete.connect(delete_muestra_callback, sender=Muestra)
post_delete.connect(delete_user_callback, sender=User)

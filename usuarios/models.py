from django.db import models
from django.contrib.auth.models import User 
import os

def get_image_path(instance, filename):
    return os.path.join('users', str(instance.username), filename)

class Usuario(User):
    
    """
        Clase que representa a los usuario del sistema.
        Atributos heredados de User y que vamos a usar:
            username: nombre de usuario
            password: password del usuario
            email: direccion de correo
            is_active: estado de la cuenta
            date_joined: fecha de registro
    """
    
    #rangoDistancia = models.IntegerField(default=1000)
    imagen = models.ImageField(upload_to=get_image_path, default='user.jpg')
    
    def __unicode__(self):
        return self.username
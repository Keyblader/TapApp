from django.db import models
from usuarios.models import Usuario
import os

# TODO: Revisar cuando el id es un numerico auto-generado.

def get_image_path_bar(instance, filename):
    return os.path.join('bares', str(instance.nombre), filename)

def get_image_path_tapa(instance, filename):
    return os.path.join('bares', str(instance.bar.nombre+instance.nombre), filename)

def get_image_path_tapa_added(instance, filename):
    ext = filename.split('.')[-1]
    if instance.id == None:
        num = Foto.objects.count() + 1
    else:
        num = instance.id 
    filename = "%s.%s" % (str(num), ext)
    return os.path.join('tapas', str(instance.tapa.id) , filename)

class Bar(models.Model):
        
    """
        Clase que representa a los bares en los que se ofrecen tapas
    """    
      
    class Meta:
        verbose_name_plural = 'Bares'  
        
    nombre = models.CharField(max_length = 100)
    descripcion = models.TextField(null = True, blank = True)
    longitud = models.CharField(max_length = 50)
    latitud = models.CharField(max_length = 50)
    imagen = models.ImageField(upload_to=get_image_path_bar, default='bar.jpg')
    fechaSubida = models.DateTimeField(auto_now=True)  
    usuarioRegistro = models.ForeignKey(Usuario)
    
    def __unicode__(self):
        return self.nombre
    
    
class Tapa(models.Model):
    
    """
        Clase que representa a las tapas que son ofrecidas en los bares
    """ 
         
    class Meta:
        unique_together = ('nombre', 'bar',)     
            
    nombre = models.CharField(max_length = 100)
    imagen = models.ImageField(upload_to=get_image_path_tapa)
    descripcion = models.TextField(null = True, blank = True)
    puntuacionMedia = models.FloatField(default=0)
    fechaSubida = models.DateTimeField(auto_now=True)    
    bar = models.ForeignKey(Bar)
    usuarioRegistro = models.ForeignKey(Usuario, related_name = 'registrador')
    favoritos = models.ManyToManyField(Usuario, related_name = 'favorito', blank = True)
    
    def __unicode__(self):
        return self.nombre
    
    
class Comentario(models.Model):

    """
        Clase que representa a los comentarios que publican los usuarios.
    """ 

    descripcion = models.TextField()    
    fechaSubida = models.DateTimeField(auto_now=True)
    tapa = models.ForeignKey(Tapa)
    usuario = models.ForeignKey(Usuario)
    
    
class Valoracion(models.Model):

    """
        Clase que representa a las valoraciones que publican los usuarios.
    """ 
    
    class Meta:
        verbose_name_plural = 'Valoraciones'
        
    puntuacion = models.IntegerField()
    tapa = models.ForeignKey(Tapa)
    usuario = models.ForeignKey(Usuario)
            
                
class Foto(models.Model):

    """
        Clase que representa a las fotos que los usuarios publican de una tapa.
    """ 
    
    imagen = models.ImageField(upload_to=get_image_path_tapa_added)
    fechaSubida = models.DateTimeField(auto_now=True)
    tapa = models.ForeignKey(Tapa)
    usuario = models.ForeignKey(Usuario)  
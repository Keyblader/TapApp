from django.db import models
from usuarios.models import Usuario
import os
from cStringIO import StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


"""
    Funciones del path de imagenes
""" 

def get_image_path_bar(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(instance.nombre), ext)
    return os.path.join('bares', str(instance.nombre), filename)

def get_image_path_bar_thumb(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s-thumb.%s" % (str(instance.nombre), ext)
    return os.path.join('bares', str(instance.nombre), filename)

def get_image_path_tapa(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ("principal", ext)
    return os.path.join('bares', str(instance.bar.nombre), str(instance.nombre), filename)

def get_image_path_tapa_added(instance, filename):
    ext = filename.split('.')[-1]
    if instance.id == None:
        num = Foto.objects.count() + 1
    else:
        num = instance.id 
    filename = "%s.%s" % (str(num), ext)
    return os.path.join('bares', str(instance.tapa.bar.nombre), str(instance.tapa.nombre), filename)


class Bar(models.Model):
        
    """
        Clase que representa a los bares en los que se ofrecen tapas
    """    
      
    class Meta:
        verbose_name_plural = 'Bares'  
        
    nombre = models.CharField(max_length = 100, unique=True)
    descripcion = models.TextField(null = True, blank = True)
    longitud = models.CharField(max_length = 50)
    latitud = models.CharField(max_length = 50)
    imagen = models.ImageField(upload_to=get_image_path_bar, default='bar.jpg')
    fechaSubida = models.DateTimeField(auto_now=True)  
    usuarioRegistro = models.ForeignKey(Usuario)
    thumbnail = models.ImageField(upload_to=get_image_path_bar_thumb, editable=False)
    
    def __unicode__(self):
        return self.nombre
    
    def create_thumbnail(self):

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.imagen:
            return

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200,200)

        DJANGO_TYPE = self.imagen.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.imagen.read()))

        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        #
        # I commented this part since it messes up my png files
        #
        #if image.mode not in ('L', 'RGB'):
        #    image = image.convert('RGB')

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.imagen.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    def save(self):
        # create a thumbnail
        self.create_thumbnail()
        super(Bar, self).save()
    
    
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
    nombre = models.CharField(max_length = 100, null=True, blank=True)
    
    
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
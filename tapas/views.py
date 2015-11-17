from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from tapas.serializers import TapaSerializer, BarSerializer, ComentarioSerializer, FotoSerializer, ValoracionSerializer
from tapas.models import Tapa, Bar, Comentario, Valoracion, Foto
from rest_framework.views import APIView
from django.http import Http404
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import math 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class TapasList(APIView):
    
    """
    Muestra un listado de las tapas ordenado por su puntuacion media.
    """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        
        tapas = Tapa.objects.all().order_by('-puntuacionMedia')

        latitudActual=request.GET.get('latitud','')
        longitudActual=request.GET.get('longitud','')
        rango=request.GET.get('rango','')
        rango=float(rango)
        print rango
        

        
        lista_tapas=[]
        latitudActual=float(latitudActual)
        longitudActual=float(longitudActual)
        
        for tapa in tapas:
        
            longitud=tapa.bar.longitud
            latitud=tapa.bar.latitud
                
            longitud=float(longitud)
            latitud=float(latitud)
        
            metrosLongitudPuntoA= longitud*(10000000/90)
            metrosLatitudPuntoA=latitud*(40000000/360)
        
            metrosLongitudActual= longitudActual*(10000000/90)
            metrosLatitudActual= latitudActual*(40000000/360)
        
            diferenciaLongitudMetros= metrosLongitudPuntoA-metrosLongitudActual
            diferenciaLatitudMetros=metrosLatitudPuntoA-metrosLatitudActual
        
            diferenciaLongitudMetros=diferenciaLongitudMetros*diferenciaLongitudMetros
            diferenciaLatitudMetros=diferenciaLatitudMetros*diferenciaLatitudMetros
        
            sumaMetros=diferenciaLatitudMetros+diferenciaLongitudMetros
        
        
            distancia= math.sqrt(sumaMetros)
            print distancia
        
        
            if distancia<rango:
                print "entra"
                lista_tapas.append(tapa) 
                
            
        
        
        # NOTA ACLARATORIA
        # unicode(request.user) == request.user.username
        # no se puede poner directamente request.user (objeto completo)
        # si se puede poner request.user.* (siendo * cualquier campo de la clase User como el id) 
        
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'serializer': TapaSerializer(lista_tapas, many=True).data
        }
        
        return Response(content)


class TapasListBar(APIView):
    
    """
    Muestra un listado de las tapas de un determinado bar.
    """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, id_bar):
        tapas = Tapa.objects.filter(bar=id_bar)
        bar = Bar.objects.get(pk=id_bar)
        
        sTapas = TapaSerializer(tapas, many=True)
        sBar = BarSerializer(bar)
        
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'tapas': sTapas.data,
            'bar': sBar.data       
        }
        
        return Response(content)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def anyadirBar(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = BarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def anyadirTapa(request):
    
    """
    Vista que nos permite crear una nueva tapa.
    """
    
    if request.method == 'POST':
        serializer = TapaSerializer(data=request.data, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def anyadirComentario(request):
    
    """
    Vista que nos permite crear un nuevo comentario.
    """
    
    if request.method == 'POST':
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
   
   
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def anyadirFoto(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = FotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

def valoracionTapa(request, id_tapa):
    t = Tapa.objects.get(pk=id_tapa)
    valoraciones = Valoracion.objects.filter(tapa=id_tapa)

    total=0.0
    if len(valoraciones) > 0:
        for valoracion in valoraciones: 
            total = total + valoracion.puntuacion
        round(total,1)
        t.puntuacionMedia = total/len(valoraciones)
    else:
        t.puntuacionMedia = 0
    t.save()


@api_view(['POST']) 
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def anyadirValoracion(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = ValoracionSerializer(data=request.data)
        if serializer.is_valid():
            tapaID = serializer.validated_data['tapa'].id
            us = User.objects.get(pk=request.user.id)
            t = Tapa.objects.get(pk=tapaID)
                                    
            try:
                valoracion = Valoracion.objects.filter(tapa=t).get(usuario=us)
                yaComentado = True
            except User.DoesNotExist:
                yaComentado = False
            except Valoracion.DoesNotExist:
                yaComentado = False
              
            if yaComentado:
                valoracion.delete() 
                 
            serializer.save()
            valoracionTapa(request, tapaID)

            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TapaDetail(APIView):
    
    """
    Muestra los detalles de una tapa.
    """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, id_tapa):
        try:
            return Tapa.objects.get(pk=id_tapa)
        except Tapa.DoesNotExist:
            raise Http404

    def get(self, request, id_tapa):
        
        t = Tapa.objects.get(pk=id_tapa)
        b = Bar.objects.get(pk=t.bar.pk)
        comentarios = Comentario.objects.filter(tapa=t)
        fotos = Foto.objects.filter(tapa=t.pk)
        
        try:
            t.favoritos.get(pk=request.user.pk)
            favorito = "true"
        except User.DoesNotExist:
            favorito = "false"      
        
        try:
            valoracion = Valoracion.objects.filter(tapa=t).get(usuario=request.user)
            puntuacion = valoracion.puntuacion
        except User.DoesNotExist:
            puntuacion = 1
        except Valoracion.DoesNotExist:
            puntuacion = 1
        
        content = {
            'user': request.user.id,  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'tapa': TapaSerializer(t).data,
            'bar': BarSerializer(b).data,
            'fotos': FotoSerializer(fotos, many=True).data,
            'comentarios': ComentarioSerializer(comentarios, many=True).data,
            'favorito': favorito,
            'puntuacion': puntuacion
        }
        
        return Response(content)
    
              
class BarDetail(APIView):
    
    """
    Devuelve una lista de los bares.
    """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, id_bar):
        try:
            return Bar.objects.get(pk=id_bar)
        except Bar.DoesNotExist:
            raise Http404

    def get(self, request, id_bar):
        
        b = Bar.objects.get(pk=id_bar) 
        tapas = Tapa.objects.filter(bar=id_bar).order_by('-puntuacionMedia')
        
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'tapas': TapaSerializer(tapas, many=True).data,
            'bar': BarSerializer(b).data,
        }
        
        return Response(content)        
    
    
@api_view(['POST']) 
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))    
def anyadirFavorito(request, id_tapa):
    t = Tapa.objects.get(pk=id_tapa)   
    try:
        t.favoritos.get(pk=request.user.pk)
        favorito = True
    except User.DoesNotExist:
        favorito = False      
    if favorito:
        t.favoritos.remove(request.user.pk)
    else: 
        t.favoritos.add(request.user.pk)    
    t.save()
    return Response(status=status.HTTP_201_CREATED)      


class BaresList(APIView):
    
    """
    Muestra un listado de los bares ordenado por su nombre.
    """
 
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        bares = Bar.objects.all().order_by('nombre')
        serializer = BarSerializer(bares, many=True)
        return Response(serializer.data)
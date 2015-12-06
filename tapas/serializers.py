from rest_framework import serializers
from tapas.models import Bar, Comentario, Foto, Tapa, Valoracion
from rest_framework.authtoken.models import Token

class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = ('id', 'nombre', 'descripcion', 'longitud', 'latitud', 'imagen', 'fechaSubida', 'usuarioRegistro')
        
class TapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tapa
        fields = ('id', 'nombre', 'imagen', 'descripcion', 'puntuacionMedia', 'fechaSubida', 'bar', 'usuarioRegistro', 'favoritos', 'nombreBar')
        
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('id', 'descripcion', 'fechaSubida', 'tapa', 'usuario', 'nombre')  
              
class ValoracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = ('id', 'puntuacion', 'tapa', 'usuario')
        
class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = ('id', 'imagen', 'fechaSubida', 'tapa', 'usuario')
        
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')             
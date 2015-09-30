from rest_framework import serializers
from usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'password', 'email', 'is_active', 'date_joined', 'imagen')
        write_only_fields = ('password',)
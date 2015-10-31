from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_active', 'date_joined')
        extra_kwargs = {
                 'password': {'write_only': True}
         }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
 
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

#===============================================================================
# from rest_framework import serializers
# from usuarios.models import Usuario
# 
# class UsuarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = ('username', 'password', 'email', 'is_active', 'date_joined', 'imagen')
#         extra_kwargs = {
#                 'password': {'write_only': True}
#         }
#         
#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
# 
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             if attr == 'password':
#                 instance.set_password(value)
#             else:
#                 setattr(instance, attr, value)
#         instance.save()
#         return instance
#===============================================================================

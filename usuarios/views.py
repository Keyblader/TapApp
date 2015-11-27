from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from usuarios.serializers import UserSerializer, UserEditSerializer
from usuarios.models import Usuario

@api_view(['POST','PUT'])
def anyadirUsuario(request):

    """
    Vista que nos permite crear un nuevo usuario.
    """

    try:
        usuario = Usuario.objects.get(username=request.user)
    except Usuario.DoesNotExist:
        print "Aun no existe"

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = UserEditSerializer(usuario,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dameUsuario(request):

    """
    Vista que nos devuelve el id del usuario.
    """

    us = Usuario.objects.get(pk=request.user.id)
    serializer = UserSerializer(us)

    content = {
            'user': request.user.id,  # `django.contrib.auth.User` instance.
            'nombre': request.user.username,
            'serializer': serializer.data
    }

    return Response(content)
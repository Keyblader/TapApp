from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from usuarios.serializers import UserSerializer

@api_view(['POST'])
def anyadirUsuario(request):
    
    """
    Vista que nos permite crear un nuevo usuario.
    """
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET'])
def dameUsuario(request):
    
    """
    Vista que nos devuelve el id del usuario.
    """
    
    content = {
            'user': request.user.id,  # `django.contrib.auth.User` instance.
    }
    
    return Response(content)
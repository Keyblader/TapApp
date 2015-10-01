from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tapas.serializers import TapaSerializer, BarSerializer, ComentarioSerializer, FotoSerializer, ValoracionSerializer

@api_view(['POST'])
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
def anyadirTapa(request):
    
    """
    Vista que nos permite crear una nueva tapa.
    """
    
    if request.method == 'POST':
        serializer = TapaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
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
 

@api_view(['POST']) 
def anyadirValoracion(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = ValoracionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Autor
from .serializers import AutorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class AutoresView(ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

@api_view(['GET', 'POST'])
def listar_autores(request):
    if request.method == 'GET':
        queryset = Autor.objects.all()
        serializer = AutorSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AutorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
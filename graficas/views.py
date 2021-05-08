#django rest framework
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

#django
from django.shortcuts import get_object_or_404

#serializers
from .serializers import *

#modelos
from .models import *


class graficasViewSet(viewsets.GenericViewSet):
    
    permission_classes = [AllowAny]

    #Parametros [mes] [ano]
    #Devolver datos con los rangos de edad y el numero de alertas en ese rango
    @action(detail=False, methods=['get'], url_path='edad-alertas')
    def edadAlertas(self,request,*args,**kwargs):
        #buscar las alertas del mes dado
        #saber la edad de cada usuaria que tuvo una alerta en este mes
        #adicionar la alerta segun el rango de edad al cual pertenezca

        serializer = edadAlertaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data,status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='alertas-mes')
    def numeroAlertaMes(self,request,*args,**kwargs):
        #parametros [mes] [ano]
        #buscar el numero de alertas en el mes y año brindados

        serializer = numeroAlertaSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        data = {
            'total_alertas_mes': serializer.save()
        }

        return Response(data,status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='horas-alertas-mes')
    def horaAlertaMes(self,request,*args,**kwargs):
        #parametros [mes] [ano] que el usuario quiera visualizar

        serializer = horaAlertaMesSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data,status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='denuncias-previas')
    def denunciasPrevias(self,request,*args,**kwargs):
        #parametros [ano]

        serializer = denunciasPreviaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='alertas-nacionalidad')
    def alertasNacionalidad(self,request,*args,**kwargs):
        #parametros [ano] [mes]

        serializer = alertasNacionalidadSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='alertas-complexion')
    def alertasComplexion(self,request,*args,**kwargs):
        #parametros [ano] [mes]

        serializer = alertasComplexionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='alertas-color-ojos')
    def colorOjo(self,request,*args,**kwargs):

        serializer = colorOjoSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='alertas-color-piel')
    def colorPiel(self,request,*args,**kwargs):
        #parametros el [ano] y [mes] que el usuario iingrese

        serializer = colorPielSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data,status=status.HTTP_200_OK)


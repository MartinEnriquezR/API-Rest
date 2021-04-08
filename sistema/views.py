#django rest framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
#serializers
from .serializers import *

"""funcion que no permite hacer login a cualquier usuario (contacto de confianza o usuaria)
    nos devuelve informacion basica del usuario y el token de acceso"""
class userLoginAPIView(APIView):
    permission_classes = [AllowAny]
    #class based view para el inicio de sesion 
    def post(self,request,*args,**kwargs):
        
        serializer = personaLoginSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        #se busca devolver los datos de la persona y el token
        persona, token = serializer.save()
        data={
            'persona': personaSerializer(persona).data,
            'access_token':token
        }
        return Response(data,status=status.HTTP_201_CREATED)

"""funcion que nos permite hacer el signup a una persona que quiere solo ser 
    contacto de confianza, devuelve informacion basica y el token de acceso"""
class personaSignupAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,*args,**kwargs):
        
        serializer = personaSignupSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        #se busca devolver los datos de la persona
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)

"""funcion que nos permite hacer el signup a una usuaria
    devuelve informacion basica y el token de acceso"""
class usuariaSignupAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,*args,**kwargs):
        serializer = usuariaSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        usuaria, token = serializer.save()
        data = {
            'usuaria' : personaSerializer(usuaria).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)

"""funcion que nos permite asociar un dispositivo rastreador con una usuaria"""
class dispositivoAsociarAPIView(APIView):
    pass

"""funcion que nos permite a la usuaria crear un grupo de confianza"""
class grupoCrearAPIView(APIView):
    pass

"""funcion que nos brinda informacion del lo grupos de confianza"""
class grupoInfoAPIView(APIView):
    pass
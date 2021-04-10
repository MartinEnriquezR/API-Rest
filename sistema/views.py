#django rest framework
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.response import Response

#serializers
from .serializers import *

#modelos 
from .models import *


"""
funcion : login (ya sea usuaria o contacto de confianza)
parametros : email y password
return : username, email, nombre, apellido_paterno, apellido_materno, 
         access_token, is_usuaria, is_contacto_cofianza
permisos : AllowAny 
"""
class personaLoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def create(self,request):
        serializer = personaLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)



"""
funcion : signup (persona)
parametros : email, username, nombre, apellido_paterno, apellido_materno
            genero, fecha_nacimiento, is_usuaria, is_contacto_confianza
return : username, email, nombre, apellido_paterno, apellido_materno, 
         access_token, is_usuaria, is_contacto_cofianza
permisos : AllowAny 
"""
class personaSignupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self,request):
        serializer = personaSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)




"""
funcion : signup (usuaria)
parametros : email, username, nombre, apellido_paterno, apellido_materno
            genero, fecha_nacimiento, is_usuaria, is_contacto_confianza
            estatura, estado_civil, escolaridad, nacionalidad, tipo_nariz
            complexion, color_ojo, forma_rostro, color_cabello, color_piel, tipo_ceja,
            textura_cabello, [enfermedades]
return : username, email, nombre, apellido_paterno, apellido_materno, 
         access_token, is_usuaria, is_contacto_cofianza
permisos : AllowAny 
"""
class usuariaSignupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self,request):
        serializer = usuariaSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)




"""prueba"""
class prueba(viewsets.ViewSet):
    
    permission_classes = [AllowAny]
    
    def list(self, request):
        queryset = Usuaria.objects.all()
        serializer = usuariaSerializer(queryset, many=True)
        return Response(serializer.data)










"""
class userLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
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
"""
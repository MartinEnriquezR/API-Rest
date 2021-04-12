#django rest framework
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
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

#permiso custom
from .permissions import *


class personaViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    
    queryset = Persona.objects.all()
    serializer_class = personaSerializer
    lookup_field = 'username'


    def get_permissions(self):
        if self.action in ['login','signup']:
            permissions = [AllowAny]
        elif self.action in ['retrieve','update','destroy','partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]


    @action(detail=False,methods=['POST'])
    def login(self,request):
        serializer = personaLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)


    @action(detail=False,methods=['POST'])
    def signup(self,request):
        serializer = personaSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)


class usuariaViewSet(mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
   
    queryset = Usuaria.objects.all()
    serializer_class = usuariaSerializer
    
    def get_permissions(self):
        if self.action in ['signup']:
            permissions = [AllowAny]
        elif self.action in ['retrieve','borrar']:
            permissions = [IsAuthenticated,IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False,methods=['POST'])
    def signup(self,request):
        serializer = usuariaSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['GET'])
    def informacion(self,request,*args,**kwargs):
        #persona = get_object_or_404(Persona,username=kwargs['pk'])
        usuaria = Usuaria.objects.get(persona=self.request.user)
        data = {
            'informacion_usuaria':usuariaSerializer(usuaria).data
        }
        return Response(data)

    @action(detail=False,methods=['DELETE'])
    def borrar(self,request,*args,**kwargs):
        usuaria = Usuaria.objects.get(persona=self.request.user)
        usuaria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,methods=['UPDATE'])
    def actualizar(self,request,*args,**kwargs):
        pass









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
"""
"""
funcion : asociar el dispositivo con la usuaria
parametros : numero de serie, pin desactivardor, [acccess_token]
return : mensaje de confirmacion con el numero de serie
permisos: Token

class dispositivoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self,request):
        queryset = DispositivoRastreador.objects.all()
        serializer = dispositivoSerializer(queryset,many=True)
        print(request.user)
        return Response(serializer.data)
    
    def partial_update(self,request,pk=None):
        data = request.data
        data['numero_serie'] = pk
        serializer = dispositivoAsociarSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
"""    
"""
class usuariaViewSet(viewsets.ModelViewSet):
    
    permission_classes = [AllowAny]
    queryset = Usuaria.objects.all()
    serializer_class = usuariaSerializer


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

"""
funcion : login (ya sea usuaria o contacto de confianza)
parametros : email y password
return : username, email, nombre, apellido_paterno, apellido_materno, 
         access_token, is_usuaria, is_contacto_cofianza
permisos : AllowAny 

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

"""
funcion : signup (persona)
parametros : email, username, nombre, apellido_paterno, apellido_materno
            genero, fecha_nacimiento, is_usuaria, is_contacto_confianza
return : username, email, nombre, apellido_paterno, apellido_materno, 
         access_token, is_usuaria, is_contacto_cofianza
permisos : AllowAny 

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
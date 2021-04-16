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


class usuariaViewSet(viewsets.GenericViewSet):
    
    #queryset = Usuaria.objects.all()

    def get_permissions(self):
        if self.action in ['signup']:
            permissions = [AllowAny]
        elif self.action in ['informacion','borrar']:
            permissions = [IsAuthenticated,IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False,methods=['post'])
    def signup(self,request,*args,**kwargs):
        serializer = usuariaSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        persona, token = serializer.save()
        data = {
            'persona' : personaSerializer(persona).data,
            'access_token' : token
        }
        return Response(data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['get'])
    def informacion(self,request,*args,**kwargs):
        usuaria = get_object_or_404(Usuaria, persona = self.request.user)
        data = usuariaSerializer(usuaria).data
        return Response(data)

    @action(detail=False,methods=['delete'])
    def borrar(self,request):
        usuaria = get_object_or_404(Usuaria, persona = self.request.user)
        usuaria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True,methods=['put','patch'])
    def actualizar(self,request,*args,**kwargs):
        prueba = self.get_object()
        partial = request.method == 'PATCH'
        print(prueba)
        return Response('hola')
    

class grupoViewSet(viewsets.GenericViewSet):
    
    def get_permissions(self):
        if self.action in ['create','retrieve','destroy','unirme','expulsar']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def create(self,request,*args,**kwargs):
        serializer = grupoCrearSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save()
        data = {
            'grupo':grupoSerializer(grupo).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self,request,*args,**kwargs):
        
        #recuperar informacion del grupo segun su usesrname
        persona = get_object_or_404(Persona,username=self.kwargs.get('pk'))
        usuaria = get_object_or_404(Usuaria, persona = persona)
        grupo = get_object_or_404(GrupoConfianza,usuaria = usuaria)

        data = {
            'informacion_grupo' : grupoInformacionSerializer(grupo).data
        }
        
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self,request,*args,**kwargs):
        #recuperar a la usuaria segun su username
        persona = get_object_or_404(Persona,username=self.kwargs.get('pk'))
        usuaria = get_object_or_404(Usuaria, persona = persona)
        grupo = get_object_or_404(GrupoConfianza,usuaria = usuaria)

        grupo.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,methods=['patch'])
    def unirme(self,request,*args,**kwargs):
        #parametros [clave de acceso] y el [username] de la persona
        self.request.data['username'] = self.kwargs.get('pk')
        partial = request.method == 'PATCH'

        serializer = grupoUnirSerializer(data = request.data, partial = partial )
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save() 

        data = {
            'grupo': grupoInformacionPersonaSerializer(grupo).data
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True,methods=['patch'])
    def expulsar(self,request,*args,**kwargs):
        #[username] de la usuaria y el [username] de la persona
        self.request.data['username_usuaria'] = self.kwargs.get('pk')
        partial = request.method == 'PATCH'

        serializer = grupoExpulsarSerializer(data = request.data, partial = partial )
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save() 

        data = {
            'grupo': grupoInformacionSerializer(grupo).data
        }

        return Response(data, status=status.HTTP_200_OK)


class dispositivoViewSet(viewsets.GenericViewSet):

    def get_permissions(self):
        if self.action in ['asociar','desasociar','cambiarpin']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=True,methods=['patch'])
    def asociar(self,request,*args,**kwargs):
        #parametros [numero_serie] y el [pin_desactivador] de la usuaria
        #obtener el username de la usuaria
        self.request.data['username'] = self.kwargs.get('pk')
        partial = request.method == 'PATCH'

        serializer = dispositivoAsociarSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        dispositivo = serializer.save()  

        data = {
            'dispositivo': dispositivoInformacionSerializer(dispositivo).data
        }

        return Response(data,status = status.HTTP_200_OK)

    @action(detail=True,methods=['patch'])
    def desasociar(self,request,*args,**kwargs):
        #datos requeridos [numero_serie] y [username] de la usuaria
        self.request.data['username'] = self.kwargs.get('pk')

        serializer = dispositivoDesasociarSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True,methods=['patch'])
    def cambiarpin(self,request,*args,**kwargs):
        #[username] de la usuaria y el [numero_serie] del dispositivo
        #[pin_desactivador] nuevo pin
        self.request.data['username'] = self.kwargs.get('pk')

        serializer = dispositivoPinSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        dispositivo = serializer.save()

        data = {
            'dispositivo' : dispositivoInformacionSerializer(dispositivo).data
        }

        return Response(data,status=status.HTTP_200_OK)
        
"""cuando la alerta se produce se envia
    [numero_serie] dispositivo rastreador
    [nombre_alerta]
    [latitud]
    [longitud]
    [fecha_hora]
"""
class alertaViewSet(viewsets.GenericViewSet):
    
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def publicar(self,request,*args,**kwargs):

        serializer = alertaPublicarSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


    """cuando se quiera  checar la desactivacion desactivar la alerta se debe enviar solo
        el [numero_serie] del dispositivo
    """
    @action(detail=False, methods=['get'])
    def desactivacion(self,request,*args,**kwargs):
        
        serializer = alertaDesactivacionSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        desactivacion = serializer.save()

        return Response(desactivacion, status = status.HTTP_200_OK)








"""
    @action(detail=True,methods=['put','patch'])
    def actualizar(self,request,*args,**kwargs):
        persona = self.get_object()
        print(persona)
        usuaria = persona.usuaria
            partial = request.methods == 'PATCH'
            serializer = usuariaSerializer(
                usuaria,
                data = request.data,
                partial = partial
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = usuariaSerializer(usuaria).data
            print(data)
        return Response('hola')
"""
"""
    @action(detail=False,methods=['GET'])
    def informacion(self,request,*args,**kwargs):
        #persona = get_object_or_404(Persona,username=kwargs['pk'])
        usuaria = get_object_or_404(Usuaria,persona=self.request.user)
        data = {
            'informacion_usuaria':usuariaSerializer(usuaria).data
        }
        return Response(data)

    @action(detail=False,methods=['DELETE'])
    def borrar(self,request):
        usuaria = Usuaria.objects.get(persona=self.request.user)
        usuaria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


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
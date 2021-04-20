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
        #se obtiene la informacion desde el token de la peticion
        usuaria = get_object_or_404(Usuaria, persona = self.request.user)
        data = usuariaSerializer(usuaria).data
        return Response(data,status=status.HTTP_200_OK)

    @action(detail=False,methods=['delete'])
    def borrar(self,request):
        
        #obtener la instancia de la persona
        persona = get_object_or_404(Persona,email=self.request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)
        
        #cambiar el estado de una usuaria
        persona.is_usuaria = False
        persona.save()
        
        #se elimina la instancia de la usuaria
        usuaria.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class dispositivoViewSet(viewsets.GenericViewSet):

    def get_permissions(self):
        if self.action in ['asociar','desasociar','cambiarpin','misDispositivos']:
            permissions = [IsAuthenticated,IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False,methods=['patch'])
    def asociar(self,request,*args,**kwargs):
        #parametros [numero_serie] y el [pin_desactivador] de la usuaria
        
        #validar que la usuaria exista dentro del sistema
        persona = get_object_or_404(Persona,email=self.request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)

        #añadir el username a los datos de request.data
        self.request.data['username'] = persona.username

        serializer = dispositivoAsociarSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        dispositivo = serializer.save()  

        data = {
            'dispositivo': dispositivoInformacionSerializer(dispositivo).data
        }

        return Response(data,status = status.HTTP_200_OK)

    @action(detail=False,methods=['patch'])
    def desasociar(self,request,*args,**kwargs):
        #datos requeridos [numero_serie]
        
        #instancia de la usuaria
        persona = get_object_or_404(Persona,email=self.request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)

        #añadir el username de la usuaria a request.data
        self.request.data['username'] = persona.username

        serializer = dispositivoDesasociarSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False,methods=['patch'])
    def cambiarpin(self,request,*args,**kwargs):
        #[numero_serie] del dispositivo y el [pin_desactivador] nuevo pin
        
        #instancia de la usuaria
        persona = get_object_or_404(Persona,email = request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)

        #añadir a request.data el username de la usuaria
        self.request.data['username'] = persona.username
        
        serializer = dispositivoPinSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        dispositivo = serializer.save()

        data = {
            'dispositivo' : dispositivoInformacionSerializer(dispositivo).data
        }

        return Response(data,status=status.HTTP_200_OK)

    @action(detail=False,methods=['get'])
    def misDispositivos(self,request,*args,**kwargs):

        #instancia de la persona
        persona = get_object_or_404(Persona,email=self.request.user)
        usuaria = get_object_or_404(Usuaria,persona=persona)
        
        #traer el dispositivo o dispositivo que tiene la usuaria
        try:
            dispositivos = DispositivoRastreador.objects.filter(usuaria=usuaria)

            serializer = dispositivoInformacionSerializer(dispositivos,many=True)
            data = serializer.data
            estado = status.HTTP_200_OK

        except DispositivoRastreador.DoesNotExist:
            data = None
            estado = status.HTTP_404_NOT_FOUND
        
        return Response(data)



class grupoViewSet(viewsets.GenericViewSet):
    
    def get_permissions(self):
        if self.action in ['create','retrieve','destroy','unirme','expulsar','nombre','misGrupos','salirGrupo']:
            permissions = [IsAuthenticated,IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def create(self,request,*args,**kwargs):
        #parametros: [nombre_grupo] del nuevo grupo

        #obtener la instancia de la usuaria
        persona = get_object_or_404(Persona,email=self.request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)

        #añadir  a request.data el username de la usuaria
        request.data['username'] = persona.username
 
        serializer = grupoCrearSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save()

        data = {
            'grupo':grupoSerializer(grupo).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self,request,*args,**kwargs):
        #no se necesitan ningun parametro

        persona = get_object_or_404(Persona, email = self.request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)
        grupo = get_object_or_404(Grupo, usuaria = usuaria)

        data = {
            'informacion_grupo' : grupoInformacionSerializer(grupo).data
        }
        
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self,request,*args,**kwargs):

        persona = get_object_or_404(Persona, email = self.request.user)
        usuaria = get_object_or_404(Usuaria, persona = persona)
        grupo = get_object_or_404(Grupo, usuaria = usuaria)

        grupo.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,methods=['patch'])
    def unirme(self,request,*args,**kwargs):
        #parametros [clave de acceso]
        
        persona = get_object_or_404(Persona, email = request.user)
        self.request.data['username'] = persona.username

        serializer = grupoUnirSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save() 

        data = {
            'grupo': grupoInformacionPersonaSerializer(grupo).data
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['patch'])
    def expulsar(self,request,*args,**kwargs):
        #parametros [username] de la persona la usuaria quiere expulsar

        persona = get_object_or_404(Persona, email=request.user)
        self.request.data['username_usuaria'] = persona.username

        serializer = grupoExpulsarSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save() 

        data = {
            'grupo': grupoInformacionSerializer(grupo).data
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['patch'])
    def nombre(self,request,*args,**kwargs):
        #[nombre] nombre del grupo nuevo

        persona = get_object_or_404(Persona, email=self.request.user)
        self.request.data['username'] = persona.username

        serializer = grupoNombreSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        grupo = serializer.save()

        data = {
            'informacion_grupo' : grupoInformacionSerializer(grupo).data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['get'],url_path='mis-grupos')
    def misGrupos(self,request,*args,**kwargs):
        
        persona = get_object_or_404(Persona,email=self.request.user)
        
        try:
            grupos = Grupo.objects.filter(integrantes__username=persona.username)
            serializer = misGruposSerializer(grupos,many=True)
            data = serializer.data
            estado = status.HTTP_200_OK
            
        except Grupo.DoesNotExist:
            data = None
            estado = status.HTTP_404_NOT_FOUND

        return Response(data, status = estado)

    @action(detail=False,methods=['patch'],url_path='salir-grupo')
    def salirGrupo(self,request,*args,**kwargs):

        #obtener la instancia de la persona que saldra del grupo
        contacto = get_object_or_404(Persona,email=self.request.user)
        
        #obtener a la admin del grupo
        admin = get_object_or_404(Persona,username=request.data['username_usuaria'])
        usuaria = get_object_or_404(Usuaria,persona=admin)
        grupo = get_object_or_404(Grupo,usuaria = usuaria)

        #salir del grupo
        miembros = get_object_or_404(Miembros,grupo=grupo,persona=contacto)
        miembros.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




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

    #se ve si la alerta fue desactivada
    @action(detail=False, methods=['get'])
    def desactivacion(self,request,*args,**kwargs):
        
        #obtener la instancia del dispositivo Dispositivo
        try:
            dispositivo = get_object_or_404(DispositivoRastreador,numero_serie=request.data['numero_serie'])
            #traer la informacion del dispositivo
            serializer = alertaDesactivacionSerializer(dispositivo)
            data = serializer.data
            estado = status.HTTP_200_OK

        except DispositivoRastreador.DoesNotExist:
            data = None
            estado = status.HTTP_404_NOT_FOUND
        
        return Response(data, status = estado)



class cuestionarioViewSet(viewsets.GenericViewSet):
    
    permission_classes = [AllowAny]

    def create(self,request,*args,**kwargs):
        #

        return Response()







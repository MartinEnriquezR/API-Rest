#django rest framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

#importando los serializers
from .serializers import *

#importando los modelos de nuestro catalogo
from .models import *

class formaRostroViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion de las formas de rostro"""
    permission_classes = [AllowAny]
    queryset = FormaRostro.objects.all()
    serializer_class = FormaRostroSerializer

class colorCabelloViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion de los colores de cabello"""
    permission_classes = [AllowAny]
    queryset = ColorCabello.objects.all()
    serializer_class = ColorCabelloSerializer

class colorPielViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion de los colores de piel"""
    permission_classes = [AllowAny]
    queryset = ColorPiel.objects.all()
    serializer_class = ColorPielSerializer

class tipoCejasViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion del tipo de cejas"""
    permission_classes = [AllowAny]
    queryset = TipoCejas.objects.all()
    serializer_class = TipoCejasSerializer

class paisViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion de los paises"""
    permission_classes = [AllowAny]
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class tipoNarizViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion del tipo de nariz"""
    permission_classes = [AllowAny]
    queryset = TipoNariz.objects.all()
    serializer_class = TipoNarizSerializer

class complexionViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion de las complexiones"""
    permission_classes = [AllowAny]
    queryset = Complexion.objects.all()
    serializer_class = ComplexionSerializer

class colorOjosViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion del color ojos"""
    permission_classes = [AllowAny]
    queryset = ColorOjos.objects.all()
    serializer_class = ColorOjosSerializer

class texturaCabelloViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar informacion de las texturas de cabello"""
    permission_classes = [AllowAny]
    queryset = TexturaCabello.objects.all()
    serializer_class = TexturaCabelloSerializer

class enfermedadViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar la informacion de las enfermedades"""
    permission_classes = [AllowAny]
    queryset = Enfermedad.objects.all()
    serializer_class = EnfermedadSerializer

class ubicacionCorporalViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar la informacion de las ubicaciones"""
    permission_classes = [AllowAny]
    queryset = UbicacionCorporal.objects.all()
    serializer_class = UbicacionCorporalSerializer

class circunstanciaViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar la informacion de las circunstancias"""
    permission_classes = [AllowAny]
    queryset = Circunstancia.objects.all()
    serializer_class = CircunstanciaSerializer

class lazoViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar la informacion de los lazos"""
    permission_classes = [AllowAny]
    queryset = Lazo.objects.all()
    serializer_class = LazoSerializer

class senasParticularesViewSet(viewsets.ReadOnlyModelViewSet):
    """un view set para listar la informacion de las señas particulares"""
    permission_classes = [AllowAny]
    queryset = SenasParticulares.objects.all()
    serializer_class = SenasParticularesSerializer

class estadoCivilViewSet(viewsets.ReadOnlyModelViewSet):
    """un viewset para listar los estados civiles de la usuaria"""
    permission_classes = [AllowAny]
    queryset = EstadoCivil.objects.all()
    serializer_class = EstadoCivilSerializer

#django rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

#importando los serializers
from .serializers import *

#importando los modelos de nuestro catalogo
from .models import *

#creacion de las vistas para enlistar la informacion de las tablas de catalogo
@api_view(['GET'])
@permission_classes([AllowAny])
def listarFormaRostro(request):
    formas = FormaRostro.objects.all()
    serializer = FormaRostroSerializer(formas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarColorCabello(request):
    color = ColorCabello.objects.all()
    serializer = ColorCabelloSerializer(color,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarColorPiel(request):
    color = ColorPiel.objects.all()
    serializer = ColorPielSerializer(color,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarTipoCejas(request):
    tipo = TipoCejas.objects.all()
    serializer = TipoCejasSerializer(tipo,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarPais(request):
    pais = Pais.objects.all()
    serializer = ColorCabelloSerializer(pais,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarTipoNariz(request):
    tipo = TipoNariz.objects.all()
    serializer = TipoNarizSerializer(tipo,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarComplexion(request):
    complexion = Complexion.objects.all()
    serializer = ComplexionSerializer(complexion,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarColorOjos(request):
    color = ColorOjos.objects.all()
    serializer = ColorOjosSerializer(color,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarTexturaCabello(request):
    textura = TexturaCabello.objects.all()
    serializer = TexturaCabelloSerializer(textura,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarEnfermedades(request):
    enfermedades = Enfermedad.objects.all()
    serializer = EnfermedadSerializer(enfermedades,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarUbicacionCorporal(request):
    ubicaciones = UbicacionCorporal.objects.all()
    serializer = UbicacionCorporalSerializer(ubicaciones,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarCircunstancia(request):
    circunstancias = Circunstancia.objects.all()
    serializer = CircunstanciaSerializer(circunstancias,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarLazo(request):
    lazos = Lazo.objects.all()
    serializer = LazoSerializer(lazos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listarSenasParticulares(request):
    senas = SenasParticulares.objects.all()
    serializer = SenasParticularesSerializer(senas,many=True)
    return Response(serializer.data)


"""
@api_view(['POST'])
def crearEnfermedad(request):
    serializer = CrearEnfermedadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    enfermedad = serializer.save()
    return Response(EnfermedadSerializer(enfermedad).data)
"""
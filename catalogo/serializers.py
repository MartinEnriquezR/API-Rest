#modelos serializados del catalogo
#se debe de crear un serializer por cada cosa que se quiere enlistar 
#se debe de crear un serializer para crear registros en la base de datos
#con is_valid se valida la informacion y se puede enviar el mensaje de error

#django rest framewok
from rest_framework import serializers

class FormaRostroSerializer(serializers.Serializer):
    forma_rostro = serializers.CharField()

class ColorCabelloSerializer(serializers.Serializer):
    color_cabello = serializers.CharField()

class ColorPielSerializer(serializers.Serializer):
    color_piel = serializers.CharField()

class TipoCejasSerializer(serializers.Serializer):
    tipo_cejas = serializers.CharField()

class PaisSerializer(serializers.Serializer):
    nombre_pais = serializers.CharField()
    nacionalidad = serializers.CharField()

class TipoNarizSerializer(serializers.Serializer):
    tipo_nariz = serializers.CharField()

class ComplexionSerializer(serializers.Serializer):
    complexion = serializers.CharField()

class ColorOjosSerializer(serializers.Serializer):
    color_ojo = serializers.CharField()

class TexturaCabelloSerializer(serializers.Serializer):
    textura_cabello = serializers.CharField()

class EnfermedadSerializer(serializers.Serializer):
    nombre_enfermedad = serializers.CharField()

class UbicacionCorporalSerializer(serializers.Serializer):
    nombre_ubicacion_corporal = serializers.CharField()

class CircunstanciaSerializer(serializers.Serializer):
    tipo_circunstancia = serializers.CharField()

class LazoSerializer(serializers.Serializer):
    lazo = serializers.CharField()

class SenasParticularesSerializer(serializers.Serializer):
    nombre_sena_particular = serializers.CharField()


"""
#importando los modelos
from .models import *

class CrearEnfermedadSerializer(serializers.Serializer):
    nombre_enfermedad = serializers.CharField(max_length=30)

    def create(self,data):
        #Crear la enfermedad
        return Enfermedad.objects.create(**data)
"""

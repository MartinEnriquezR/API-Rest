#modelos serializados del catalogo
#se debe de crear un serializer por cada cosa que se quiere enlistar 
#se debe de crear un serializer para crear registros en la base de datos
#con is_valid se valida la informacion y se puede enviar el mensaje de error

#django rest framewok
from rest_framework import serializers

#modelos de catalogo
from .models import *

class FormaRostroSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaRostro
        fields = ('forma_rostro',)

class ColorCabelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorCabello
        fields = ('color_cabello',)

class ColorPielSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPiel
        fields = ('color_piel',)

class TipoCejasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCejas
        fields = ('tipo_ceja',)

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ('nombre_pais','nacionalidad',)
    
class TipoNarizSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNariz
        fields = ('tipo_nariz',)

class ComplexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexion
        fields = ('complexion',)

class ColorOjosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorOjos
        fields = ('color_ojo',)

class TexturaCabelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexturaCabello
        fields = ('textura_cabello',)

class EnfermedadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Enfermedad
        fields = ['nombre_enfermedad']

class UbicacionCorporalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbicacionCorporal
        fields = ('nombre_ubicacion_corporal',)

class CircunstanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circunstancia 
        fields = ('tipo_circunstancia',)

class LazoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lazo 
        fields = ('lazo',)
        
class SenasParticularesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenasParticulares
        fields = ('nombre_sena_particular',)

class EstadoCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCivil
        fields = ('estado_civil',)
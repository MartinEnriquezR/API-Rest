from django.db import models

class FormaRostro(models.Model):
    forma_rostro = models.CharField(max_length=30)

    class Meta:
        db_table = 'FORMA_ROSTRO'

class ColorCabello(models.Model):
    color_cabello = models.CharField(max_length=20)

    class Meta:
        db_table = 'COLOR_CABELLO'

class ColorPiel(models.Model):
    color_piel = models.CharField(max_length=30)

    class Meta:
        db_table = 'COLOR_PIEL'

class TipoCejas(models.Model):
    tipo_ceja = models.CharField(max_length=15)

    class Meta:
        db_table = 'TIPO_CEJAS'

class Pais(models.Model):
    nombre_pais = models.CharField(max_length=30)
    nacionalidad = models.CharField(max_length=30)

    class Meta:
        db_table = 'PAIS'

class TipoNariz(models.Model):
    tipo_nariz = models.CharField(max_length=30)

    class Meta:
        db_table = 'TIPO_NARIZ'

class Complexion(models.Model):
    complexion = models.CharField(max_length=20)

    class Meta:
        db_table = 'COMPLEXION'

class ColorOjos(models.Model):
    color_ojo = models.CharField(max_length=20)

    class Meta:
        db_table = 'COLOR_OJOS'

class TexturaCabello(models.Model):
    textura_cabello = models.CharField(max_length=30)

    class Meta:
        db_table = 'TEXTURA_CABELLO'

class Enfermedad(models.Model):
    nombre_enfermedad = models.CharField(max_length=30)

    class Meta:
        db_table = 'ENFERMEDAD'

class UbicacionCorporal(models.Model):
    nombre_ubicacion_corporal = models.CharField(max_length=30)

    class Meta:
        db_table = 'UBICACION_CORPORAL'

class Circunstancia(models.Model):
    tipo_circunstancia = models.CharField(max_length=100)

    class Meta:
        db_table = 'CIRCUNSTANCIA'

class Lazo(models.Model):
    lazo = models.CharField(max_length=30)

    class Meta:
        db_table = 'LAZO'

class SenasParticulares(models.Model):
    nombre_sena_particular = models.CharField(max_length=20)

    class Meta:
        db_table = 'SENAS_PARTICULARES'

class EstadoCivil(models.Model):
    estado_civil = models.CharField(max_length=30)

    class Meta:
        db_table = 'ESTADO_CIVIL'
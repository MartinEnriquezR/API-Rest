# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alerta(models.Model):
    id_alerta = models.IntegerField(primary_key=True)
    id_grupo_confianza = models.ForeignKey('GrupoConfianza', models.DO_NOTHING, db_column='id_grupo_confianza')

    class Meta:
        managed = False
        db_table = 'alerta'


class AlertaAudit(models.Model):
    id_alerta_audit = models.IntegerField(blank=True, null=True)
    id_grupo_confianza = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alerta_audit'


class Circunstancia(models.Model):
    id_circunstancia = models.IntegerField(primary_key=True)
    tipo_circunstancia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'circunstancia'


class ColorCabello(models.Model):
    id_color_cabello = models.IntegerField(primary_key=True)
    color_cabello = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'color_cabello'


class ColorOjos(models.Model):
    id_color_ojo = models.IntegerField(primary_key=True)
    colo_ojo = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'color_ojos'


class ColorPiel(models.Model):
    id_color_piel = models.IntegerField(primary_key=True)
    color_piel = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'color_piel'


class Complexion(models.Model):
    id_complexion = models.IntegerField(primary_key=True)
    complexion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'complexion'


class Cuestionario(models.Model):
    id_cuestionario = models.IntegerField(primary_key=True)
    id_contacto_confianza = models.IntegerField()
    descripcion = models.CharField(max_length=2000, blank=True, null=True)
    autoridad_denuncia = models.CharField(max_length=50, blank=True, null=True)
    modelo_vehiculo = models.CharField(max_length=50, blank=True, null=True)
    violencia = models.CharField(max_length=2, blank=True, null=True)
    acompanar = models.CharField(max_length=2, blank=True, null=True)
    denuncia_previa = models.CharField(max_length=2, blank=True, null=True)
    manejaba_auto = models.CharField(max_length=2, blank=True, null=True)
    id_alerta = models.ForeignKey(Alerta, models.DO_NOTHING, db_column='id_alerta')
    id_circunstancia = models.ForeignKey(Circunstancia, models.DO_NOTHING, db_column='id_circunstancia')
    id_lazo = models.ForeignKey('Lazo', models.DO_NOTHING, db_column='id_lazo')

    class Meta:
        managed = False
        db_table = 'cuestionario'


class CuestionarioAudit(models.Model):
    id_cuestionario_audit = models.IntegerField(blank=True, null=True)
    violencia = models.CharField(max_length=2, blank=True, null=True)
    denuncia_previa = models.CharField(max_length=2, blank=True, null=True)
    id_alerta_audit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuestionario_audit'


class DispositivoRastreador(models.Model):
    numero_serie = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    pin_desactivador = models.IntegerField(blank=True, null=True)
    id_usuaria = models.ForeignKey('Usuaria', models.DO_NOTHING, db_column='id_usuaria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivo_rastreador'


class Enfermedad(models.Model):
    id_enfermedad = models.IntegerField(primary_key=True)
    nombre_enfermedad = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'enfermedad'


class FormaRostro(models.Model):
    id_forma_rostro = models.IntegerField(primary_key=True)
    forma_rostro = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'forma_rostro'


class GrupoConfianza(models.Model):
    id_grupo_confianza = models.IntegerField(primary_key=True)
    nombre_grupo = models.CharField(max_length=20)
    clave_acceso = models.CharField(max_length=6)
    id_usuaria = models.ForeignKey('Usuaria', models.DO_NOTHING, db_column='id_usuaria')

    class Meta:
        managed = False
        db_table = 'grupo_confianza'


class GrupoConfianzaAudit(models.Model):
    id_grupo_confianza_audit = models.IntegerField(blank=True, null=True)
    id_usuaria_audit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupo_confianza_audit'


class GrupoConfianzaHasContactoConfianza(models.Model):
    id_grupo_confianza = models.OneToOneField(GrupoConfianza, models.DO_NOTHING, db_column='id_grupo_confianza', primary_key=True)
    id_contacto_confianza = models.ForeignKey('Persona', models.DO_NOTHING, db_column='id_contacto_confianza')

    class Meta:
        managed = False
        db_table = 'grupo_confianza_has_contacto_confianza'
        unique_together = (('id_grupo_confianza', 'id_contacto_confianza'),)


class Lazo(models.Model):
    id_lazo = models.IntegerField(primary_key=True)
    lazo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lazo'


class Pais(models.Model):
    id_pais = models.IntegerField(primary_key=True)
    nombre_pais = models.CharField(max_length=30)
    nacionalidad = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'pais'


class Persona(models.Model):
    id_persona = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=15)
    apellido_materno = models.CharField(max_length=15)
    genero = models.CharField(max_length=15)
    correo = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    pass_hash = models.CharField(max_length=40)
    pass_salt = models.CharField(max_length=8)
    is_usuaria = models.BooleanField()
    is_contacto_confianza = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'persona'


class PersonaAudit(models.Model):
    id_persona_audit = models.IntegerField(blank=True, null=True)
    genero = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    is_usuaria = models.BooleanField(blank=True, null=True)
    is_contacto_confianza = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persona_audit'


class SenasParticulares(models.Model):
    id_sena_particular = models.IntegerField(primary_key=True)
    nombre_sena_particular = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'senas_particulares'


class TexturaCabello(models.Model):
    id_textura_cabello = models.IntegerField(primary_key=True)
    textura_cabello = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'textura_cabello'


class TipoCejas(models.Model):
    id_tipo_ceja = models.IntegerField(primary_key=True)
    tipo_ceja = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'tipo_cejas'


class TipoNariz(models.Model):
    id_tipo_nariz = models.IntegerField(primary_key=True)
    tipo_nariz = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_nariz'


class Ubicacion(models.Model):
    id_ubicacion = models.IntegerField(primary_key=True)
    latitud = models.DecimalField(max_digits=8, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    id_alerta = models.ForeignKey(Alerta, models.DO_NOTHING, db_column='id_alerta')

    class Meta:
        managed = False
        db_table = 'ubicacion'


class UbicacionAudit(models.Model):
    id_ubicacion_audit = models.IntegerField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicacion_audit'


class UbicacionCorporal(models.Model):
    id_ubicacion_corporal = models.IntegerField(primary_key=True)
    nombre_ubicacion_corporal = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ubicacion_corporal'


class Usuaria(models.Model):
    id_usuaria = models.OneToOneField(Persona, models.DO_NOTHING, db_column='id_usuaria', primary_key=True)
    estatura = models.IntegerField()
    estado_civil = models.CharField(max_length=20)
    escolaridad = models.CharField(max_length=30)
    id_pais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='id_pais')
    id_tipo_nariz = models.ForeignKey(TipoNariz, models.DO_NOTHING, db_column='id_tipo_nariz')
    id_complexion = models.ForeignKey(Complexion, models.DO_NOTHING, db_column='id_complexion')
    id_color_ojo = models.ForeignKey(ColorOjos, models.DO_NOTHING, db_column='id_color_ojo')
    id_forma_rostro = models.ForeignKey(FormaRostro, models.DO_NOTHING, db_column='id_forma_rostro')
    id_color_cabello = models.ForeignKey(ColorCabello, models.DO_NOTHING, db_column='id_color_cabello')
    id_color_piel = models.ForeignKey(ColorPiel, models.DO_NOTHING, db_column='id_color_piel')
    id_tipo_ceja = models.ForeignKey(TipoCejas, models.DO_NOTHING, db_column='id_tipo_ceja')
    id_textura_cabello = models.ForeignKey(TexturaCabello, models.DO_NOTHING, db_column='id_textura_cabello')

    class Meta:
        managed = False
        db_table = 'usuaria'


class UsuariaAudit(models.Model):
    id_usuaria_audit = models.IntegerField(blank=True, null=True)
    id_pais = models.IntegerField(blank=True, null=True)
    id_complexion = models.IntegerField(blank=True, null=True)
    id_color_piel = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuaria_audit'


class UsuariaHasEnfermedad(models.Model):
    id_enfermedad = models.OneToOneField(Enfermedad, models.DO_NOTHING, db_column='id_enfermedad', primary_key=True)
    id_usuaria = models.ForeignKey(Usuaria, models.DO_NOTHING, db_column='id_usuaria')

    class Meta:
        managed = False
        db_table = 'usuaria_has_enfermedad'
        unique_together = (('id_enfermedad', 'id_usuaria'),)


class UsuariaHasSenaUbicacion(models.Model):
    id_ubicacion_corporal = models.OneToOneField(UbicacionCorporal, models.DO_NOTHING, db_column='id_ubicacion_corporal', primary_key=True)
    id_sena_particular = models.ForeignKey(SenasParticulares, models.DO_NOTHING, db_column='id_sena_particular')
    id_usuaria = models.ForeignKey(Usuaria, models.DO_NOTHING, db_column='id_usuaria')
    descripcion = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'usuaria_has_sena_ubicacion'
        unique_together = (('id_ubicacion_corporal', 'id_sena_particular', 'id_usuaria'),)

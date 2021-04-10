#librerias de django
from django.db import models
from django.contrib.auth.models import AbstractUser

#modelos del catalogo
from catalogo.models import *

#tabla revisada sin llaves foraneas
class Persona(AbstractUser):
    email = models.EmailField(
        'email_address',
        unique=True,
        error_messages={
            'unique':'Un usuario ya se encuentra registrado con este correo'
        }
    )
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=15)
    apellido_materno = models.CharField(max_length=15)
    genero = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    is_usuaria = models.BooleanField()
    is_contacto_confianza = models.BooleanField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'username',
        'genero',
        'fecha_nacimiento',
        'is_usuaria',
        'is_contacto_confianza'
    ]

    class Meta:
        db_table='PERSONA'

#al ser borrada la persona se borra la usuaria
#si se borran las tablas de catalogo no se debe de hacer nada
class Usuaria(models.Model):
    persona = models.OneToOneField(Persona, on_delete = models.CASCADE)
    #datos de complemento
    estatura = models.PositiveIntegerField()
    estado_civil = models.CharField(max_length=20)
    escolaridad = models.CharField(max_length=30)
    #llaves foraneas
    pais = models.ForeignKey(Pais, models.DO_NOTHING)
    tipo_nariz = models.ForeignKey(TipoNariz, models.DO_NOTHING)
    complexion = models.ForeignKey(Complexion, models.DO_NOTHING)
    color_ojo = models.ForeignKey(ColorOjos, models.DO_NOTHING)
    forma_rostro = models.ForeignKey(FormaRostro, models.DO_NOTHING)
    color_cabello = models.ForeignKey(ColorCabello, models.DO_NOTHING)
    color_piel = models.ForeignKey(ColorPiel, models.DO_NOTHING)
    tipo_ceja = models.ForeignKey(TipoCejas, models.DO_NOTHING)
    textura_cabello = models.ForeignKey(TexturaCabello, models.DO_NOTHING)
    enfermedades = models.ManyToManyField(Enfermedad)
    #campos requeridos
    REQUIRED_FIELDS=[
        'estatura',
        'estado_civil',
        'escolaridad',
        'pais',
        'tipo_nariz',
        'complexion,'
        'color_ojo',
        'forma_rostro',
        'forma_rostro',
        'id_color_cabello',
        'id_color_piel',
        'id_tipo_ceja',
        'id_textura_cabello'
    ]

    class Meta:
        db_table = 'USUARIA'  

#cuando la usuaria se da de baja el dispositivo rastreador no se borra
class DispositivoRastreador(models.Model):
    
    numero_serie = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    pin_desactivador = models.IntegerField(blank=True, null=True)
    #llaves foraneas
    usuaria = models.ForeignKey(Usuaria, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'DISPOSITIVO_RASTREADOR'

    REQUIRED_FIELDS=[
        'numero_serie',
        'estado',
        'pin_desactivador',
        'usuaria'
    ]

#cuando la usuaria se de de baja del sistema su grupo de confianza tambien se borra
class GrupoConfianza(models.Model):
    usuaria = models.OneToOneField('Usuaria', on_delete=models.CASCADE)
    nombre_grupo = models.CharField(max_length = 20)
    clave_acceso = models.CharField(max_length = 6, unique = True)
    miembros = models.ManyToManyField(Persona)

    class Meta:
        db_table = 'GRUPO_CONFIANZA'
    
    REQUIRED_FIELDS=[
        'nombre_grupo',
        'clave_acceso',
        'usuaria'
    ]

#cuando el grupo se borra, las alertas se deben de borrar
class Alerta(models.Model):
    grupo_confianza = models.ForeignKey(GrupoConfianza, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ALERTA'

    REQUIRED_FIELDS=['grupo_confianza']

#cuando la alerta se borra, el cuestionario se debe de borrar
#cuando una circunstancia se borre no se debe de hacer nada
#cuando un lazo se borre no se debe de hacer nada 
class Cuestionario(models.Model):
    
    contacto_confianza = models.IntegerField()
    descripcion = models.CharField(max_length=2000, blank=True, null=True)
    autoridad_denuncia = models.CharField(max_length=50, blank=True, null=True)
    modelo_vehiculo = models.CharField(max_length=50, blank=True, null=True)
    violencia = models.CharField(max_length=2, blank=True, null=True)
    acompanar = models.CharField(max_length=2, blank=True, null=True)
    denuncia_previa = models.CharField(max_length=2, blank=True, null=True)
    manejaba_auto = models.CharField(max_length=2, blank=True, null=True)
    #llaves foraneas
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    circunstancia = models.ForeignKey(Circunstancia, models.DO_NOTHING)
    lazo = models.ForeignKey(Lazo, models.DO_NOTHING)

    class Meta:
        db_table = 'CUESTIONARIO'

    REQUIRED_FIELDS=[
        'contacto_confianza',
        'alerta',
        'circunstancia',
        'lazo'
    ]

#si se borra la alerta, las ubicaciones se deben de borrar
class Ubicacion(models.Model):

    latitud = models.DecimalField(max_digits=8, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    #llave foranea
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UBICACION'

    REQUIRED_FIELDS=[
        'latitud',
        'longitud',
        'fecha_hora',
        'alerta'
    ]

#si la ubicacion corporal se borra no se debe de hacer nada
#si la sena se borra no se debe de hacer nada
#si la usuaria se borra el registro se debe de borrar
class UsuariaHasSenaUbicacion(models.Model):
    
    ubicacion_corporal = models.ForeignKey(UbicacionCorporal, models.DO_NOTHING)
    sena_particular = models.ForeignKey(SenasParticulares, models.DO_NOTHING)
    usuaria = models.ForeignKey(Usuaria, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)

    class Meta:
        db_table = 'USUARIA_HAS_SENA_UBICACION'
        unique_together = (('ubicacion_corporal', 'sena_particular', 'usuaria'))

    REQUIRED_FIELDS=[
        'ubicacion_corporal',
        'sena_particular',
        'usuaria',
        'descripcion',
    ]


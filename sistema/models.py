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
        'genero',
        'fecha_nacimiento',
        'is_usuaria',
        'is_contacto_confianza', 
        'username'
    ]

    class Meta:
        db_table='PERSONA'

#al ser borrada la persona se borra la usuaria
#si se borran las tablas de catalogo no se debe de hacer nada
class Usuaria(models.Model):
    persona = models.OneToOneField(Persona, on_delete = models.CASCADE)
    #datos de complemento
    estatura = models.PositiveIntegerField()
    estado_civil = models.ForeignKey(EstadoCivil, models.DO_NOTHING)
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
        'color_cabello',
        'color_piel',
        'tipo_ceja',
        'textura_cabello',
        'enfermedades'
    ]

    class Meta:
        db_table = 'USUARIA'  

#cuando la usuaria se da de baja el dispositivo rastreador no se borra
class DispositivoRastreador(models.Model):
    
    numero_serie = models.IntegerField(primary_key=True)
    pin_desactivador = models.IntegerField(blank=True, null=True)
    #llaves foraneas
    usuaria = models.ForeignKey(Usuaria, models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'DISPOSITIVO_RASTREADOR'

    REQUIRED_FIELDS=[
        'numero_serie',
        'pin_desactivador',
        'usuaria'
    ]

#cuando la usuaria se de de baja del sistema su grupo de confianza tambien se borra
class Grupo(models.Model):
    #quien administra el grupo
    usuaria = models.OneToOneField('Usuaria', on_delete=models.CASCADE)
    nombre = models.CharField(max_length = 20)
    clave_acceso = models.CharField(max_length = 6, unique = True)
    estado_alerta = models.BooleanField(default=False)
    integrantes = models.ManyToManyField(Persona, through='Miembros', blank=True)

    class Meta:
        db_table = 'GRUPO'
    
    REQUIRED_FIELDS=[
        'nombre',
        'clave_acceso',
        'estado_alerta',
        'usuaria'
    ]

#tabla con los miembros que se añaden al grupo
class Miembros(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE)
    persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
    fecha_union = models.DateField()

    class Meta:
        db_table = 'MIEMBROS'

    REQUIRED_FIELDS=[
        'grupo',
        'persona',
        'fecha_union',
    ]

#cuando el grupo se borra, las alertas se deben de borrar
class Alerta(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    nombre_alerta = models.CharField(max_length=30)
    fecha_hora = models.DateTimeField()

    class Meta:
        db_table = 'ALERTA'

    REQUIRED_FIELDS=['grupo','nombre_alerta','fecha_hora']

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


#cuando la alerta se borra, el cuestionario se debe de borrar
#cuando una circunstancia se borre no se debe de hacer nada
#cuando un lazo se borre no se debe de hacer nada 
class Cuestionario(models.Model):
    
    miembro = models.ForeignKey(Miembros, on_delete=models.CASCADE)
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)

    descripcion = models.CharField(max_length=2000, blank=True, null=True)
    autoridad_denuncia = models.CharField(max_length=50, blank=True, null=True)
    modelo_vehiculo = models.CharField(max_length=50, blank=True, null=True)
    violencia = models.CharField(max_length=2, blank=True, null=True)
    acompanar = models.CharField(max_length=2, blank=True, null=True)
    denuncia_previa = models.CharField(max_length=2, blank=True, null=True)
    manejaba_auto = models.CharField(max_length=2, blank=True, null=True)
    estado_usuaria = models.CharField(max_length=15)

    #llaves foraneas para complementar el cuestionario
    circunstancia = models.ForeignKey(Circunstancia, models.DO_NOTHING)
    lazo = models.ForeignKey(Lazo, models.DO_NOTHING)

    class Meta:
        db_table = 'CUESTIONARIO'

    REQUIRED_FIELDS=[
        'username',
        'contacto_confianza',
        'estado_usuaria',
        'alerta',
        'circunstancia',
        'lazo'
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


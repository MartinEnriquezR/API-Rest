#django
from django.contrib.auth import authenticate, password_validation

#librearia de date
from datetime import date

#django rest framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

#librerias de python
from random import seed
from random import randint

#importando los modelos
from .models import *

#importando los modelos de catalogo
from catalogo.models import *

#Modelserializers del catalogo
from catalogo.serializers import *


"""finalizado"""
class personaSerializer(serializers.ModelSerializer):
    #modelo serializado 
    class Meta:
        model = Persona
        fields = (
            'email',
            'username',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'genero',
            'fecha_nacimiento',
            'is_usuaria',
            'is_contacto_confianza'
        )

"""finalizado"""
class personaLoginSerializer(serializers.Serializer):
    #definimos los campos que seran validados y sus limitantes
    email=serializers.EmailField()
    password=serializers.CharField(min_length=8)
 
    def validate(self,data):
        #validacion de todos los datos 
        #se ejecuta despues de que se validaron los datos necesarios
        #se usa la autentificacion de django
        persona = authenticate(username=data['email'],password=data['password'])
        if not persona:
            raise serializers.ValidationError('Credenciales invalidas')

        #cada serializer tiene un context, que es como un atributo de una clase
        # arriba ya se tiene la instancia de persona 
        self.context['persona'] = persona
        return data

    def create(self,data):
        #genera o devuelve el token de la persona (usuaria o contacto de confianza)
        token, created = Token.objects.get_or_create(user=self.context['persona'])
        return self.context['persona'], token.key

"""finalizado"""
class personaSignupSerializer(serializers.Serializer):
    #campos que debemos de aceptar 
    email=serializers.EmailField(
        validators=[
            UniqueValidator(queryset=Persona.objects.all())
        ]
    )
    username=serializers.CharField(
        min_length=4,
        max_length=16,
        validators=[
            UniqueValidator(queryset=Persona.objects.all())
        ]
    )
    password=serializers.CharField(min_length=8)
    password_confirmation=serializers.CharField(min_length=8)
    nombre=serializers.CharField(max_length=30)
    apellido_paterno=serializers.CharField(max_length=15)
    apellido_materno=serializers.CharField(max_length=15)
    genero=serializers.CharField(max_length=15)
    fecha_nacimiento=serializers.DateField()
    is_usuaria=serializers.BooleanField()
    is_contacto_confianza=serializers.BooleanField()

    def validate(self,data):
        #validar la contraseña
        passwd = data['password']
        passwdConf = data['password_confirmation']
        #validar que las contraseñas sean iguales
        if passwd != passwdConf:
            raise serializers.ValidationError('las contraseñas ingresadas no coinciden')
        password_validation.validate_password(passwd)
        return(data)
    
    def create(self,data):
        #se remueve de data el excedente de informacion 
        data.pop('password_confirmation')
        #se registra a la persona 
        persona = Persona.objects.create_user(**data)
        #se obtiene la instancia de la persona
        self.context['persona'] = persona
        token, created = Token.objects.get_or_create(user=self.context['persona'])
        return persona, token.key

"""finalizado"""
class usuariaSignupSerializer(serializers.Serializer):
    
    #datos de la persona
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=Persona.objects.all())
        ]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=16,
        validators=[
            UniqueValidator(queryset=Persona.objects.all())
        ]
    )
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8)
    nombre = serializers.CharField(max_length=30)
    apellido_paterno = serializers.CharField(max_length=15)
    apellido_materno = serializers.CharField(max_length=15)
    genero = serializers.CharField(max_length=15)
    fecha_nacimiento = serializers.DateField()
    is_usuaria = serializers.BooleanField()
    is_contacto_confianza = serializers.BooleanField()
    #campos de la usuaria  
    estatura = serializers.IntegerField()
    estado_civil = serializers.CharField(max_length=20)
    escolaridad = serializers.CharField(max_length=30)
    #llaves foraneas
    nacionalidad = serializers.CharField()
    tipo_nariz = serializers.CharField()
    complexion = serializers.CharField()
    color_ojo = serializers.CharField()
    forma_rostro = serializers.CharField()
    color_cabello = serializers.CharField()
    color_piel = serializers.CharField()
    tipo_ceja = serializers.CharField()
    textura_cabello = serializers.CharField()

    enfermedades = EnfermedadSerializer(many=True)


    def validate(self,data):
        """validacion los datos de la persona"""

        passwd = data['password']
        passwdConf = data['password_confirmation']
        genero = data['genero']
        fecha_nacimiento = data['fecha_nacimiento']
        today = date.today()
        diferenciaDias = today - fecha_nacimiento

        #validar que las contraseñas, deben ser iguales
        if passwd != passwdConf:
            raise serializers.ValidationError('las contraseñas ingresadas no coinciden')
        #valida que la contraseña no sea comun
        password_validation.validate_password(passwd)


        #validar que el genero sea femenino
        if genero != 'Femenino':
            raise serializers.ValidationError('el genero de la usuaria debe de ser femenino')
        
        
        #validar que la usuaria tenga  al menos 15 años 
        if diferenciaDias.days < 5475:
            raise serializers.ValidationError('La usuaria debe de tener al menos 15 años cumplidos.')
        
        #validar que los datos existan dentro de la base de datos
        try:
            nacionalidad = Pais.objects.get(nacionalidad=data['nacionalidad'])
        except Pais.DoesNotExist:
            raise serializers.ValidationError('Este pais no se encuentra registrado')

        try:
            tipo_nariz = TipoNariz.objects.get(tipo_nariz=data['tipo_nariz'])
        except TipoNariz.DoesNotExist:
            raise serializers.ValidationError('Este tipo de nariz no se encuentra registrado')

        try:
            complexion = Complexion.objects.get(complexion=data['complexion'])
        except Complexion.DoesNotExist:
            raise serializers.ValidationError('Esta complexion no esta registrada')

        try:
            color_ojo = ColorOjos.objects.get(color_ojo=data['color_ojo'])
        except ColorOjos.DoesNotExist:
            raise serializers.ValidationError('Esta color de ojos no esta registrado')

        try:
            forma_rostro = FormaRostro.objects.get(forma_rostro=data['forma_rostro'])
        except FormaRostro.DoesNotExist:
            raise serializers.ValidationError('Esta forma de rostro no se encuentra registrada')
        
        try:
            color_cabello = ColorCabello.objects.get(color_cabello=data['color_cabello'])
        except ColorCabello.DoesNotExist:
            raise serializers.ValidationError('Este color de cabello no se encuentra registrado')

        try:
            color_piel = ColorPiel.objects.get(color_piel=data['color_piel'])
        except ColorPiel.DoesNotExist:
            raise serializers.ValidationError('Este color de piel no se encuentra registrado')

        try:
            tipo_ceja = TipoCejas.objects.get(tipo_ceja=data['tipo_ceja'])
        except TipoCejas.DoesNotExist:
            raise serializers.ValidationError('Este tipo de cejas no se encuentran registradas')

        try:
            textura_cabello = TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])
        except TexturaCabello.DoesNotExist:
            raise serializers.ValidationError('Este tipo de cabello no se encuentran registrado')

        return(data)
  

    def create(self,data):

        #claves de los datos de la persona  
        personaKeys = [
            'email',
            'username',
            'password',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'genero', 
            'fecha_nacimiento',
            'is_usuaria',
            'is_contacto_confianza'
        ]
        #datos de la persona
        dataPersona = { index : data[index] for index in personaKeys }
        #registro de la persona 
        persona = Persona.objects.create_user(**dataPersona)

        #claves de los datos de la usuaria
        usuariaKeys = [
            'estatura',
            'estado_civil',
            'escolaridad'
        ]
        #datos de la usuaria
        dataUsuaria = { index : data[index] for index in usuariaKeys }

        #registro de la usuaria
        usuaria = Usuaria.objects.create(
            #instancia de la persona
            persona = persona, 
            #datos de la usuaria 
            **dataUsuaria,
            #llaves foraneas de la usuaria
            pais=Pais.objects.get(nacionalidad=data['nacionalidad']),
            tipo_nariz=TipoNariz.objects.get(tipo_nariz=data['tipo_nariz']),
            complexion=Complexion.objects.get(complexion=data['complexion']),
            color_ojo=ColorOjos.objects.get(color_ojo=data['color_ojo']),
            forma_rostro=FormaRostro.objects.get(forma_rostro=data['forma_rostro']),
            color_cabello=ColorCabello.objects.get(color_cabello=data['color_cabello']),
            color_piel=ColorPiel.objects.get(color_piel=data['color_piel']),
            tipo_ceja=TipoCejas.objects.get(tipo_ceja=data['tipo_ceja']),
            textura_cabello=TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])
            #enfermedades=
        )
        
        #registro de la o las enfermedades que padece la usuaria
        enfermedades = data.pop('enfermedades')
        for enfermedadData in enfermedades:
            usuaria.enfermedades.add(
                #objeto de la enfermedad
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
            )
        
        #obtener el token
        self.context['persona'] = persona
        token, created = Token.objects.get_or_create(user=self.context['persona'])
        return persona, token.key

"""finalizado"""
class usuariaSerializer(serializers.ModelSerializer):
    persona = serializers.EmailField()
    pais = PaisSerializer()
    tipo_nariz = TipoNarizSerializer()
    complexion = ComplexionSerializer()
    color_ojo = ColorOjosSerializer()
    forma_rostro = FormaRostroSerializer()
    color_cabello = ColorCabelloSerializer()
    color_piel = ColorPielSerializer()
    tipo_ceja = TipoCejasSerializer()
    textura_cabello = TexturaCabelloSerializer()
    enfermedades = EnfermedadSerializer(many=True)

    class Meta:
        model = Usuaria
        fields = (
            'persona',
            'estatura',
            'estado_civil',
            'escolaridad',
            'pais',
            'tipo_nariz',
            'complexion',
            'color_ojo',
            'forma_rostro',
            'color_cabello',
            'color_piel',
            'tipo_ceja',
            'textura_cabello',
            'enfermedades'
        )
    
"""finalizado"""
class grupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoConfianza
        fields = (
            'nombre_grupo',
            'clave_acceso'
        )

"""finalizado"""
class grupoCrearSerializer(serializers.Serializer):
    #validar el tamaño del nombre del grupo
    username = serializers.CharField()
    nombre_grupo = serializers.CharField(max_length=20)
    
    def validate(self,data):
        
        #verificar que no se haya excedido el maximo numero de grupo permitidos
        grupos = GrupoConfianza.objects.all().count()
        if grupos == 1000000:
            raise serializers.ValidationError('Ya no existen grupos disponibles')
        
        #verificar que la usuaria no tenga un grupo ya existente
        try:
            persona = Persona.objects.get(username =data['username'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username invalido')

        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Usuario invalido')

        try:
            grupo = GrupoConfianza.objects.get(usuaria=usuaria)
            raise serializers.ValidationError('La usuaria ya tiene un grupo de confianza')
        except GrupoConfianza.DoesNotExist:
            pass

        #validar la clave de acceso, que no este en uso por otro grupo
        seed(1)
        while True:
            clave = randint(0,999999)
            try:
                GrupoConfianza.objects.get(clave_acceso=str(clave))
            except GrupoConfianza.DoesNotExist:
                self.context['clave'] = str(clave)
                break

        return(data)
    
    def create(self,data):
        #obtener a la usuaria
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #guardar la informacion
        data.pop('username')
        grupo = GrupoConfianza.objects.create(
            **data,
            usuaria = usuaria,
            clave_acceso = self.context['clave']
        )

        return grupo

"""finalizado"""
class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            'username',
            'nombre',
            'apellido_paterno',
            'apellido_materno'
        )

"""finalizado"""
class grupoInformacionSerializer(serializers.ModelSerializer):
    miembros = MiembroSerializer(many=True)

    class Meta:
        model = GrupoConfianza
        fields = (
            'nombre_grupo',
            'clave_acceso',
            'miembros'
        )







"""
class dispositivoAsociarSerializer(serializers.Serializer):
    numero_serie = serializers.IntegerField()
    pin_desactivador = serializers.IntegerField()
    estado=serializers.CharField(max_length=20)
    email = serializers.EmailField()

    def validate(self, data):
        #buscar si el dispositivo se encuentra dentro de la base de datos
        try:
            registrado = DispositivoRastreador.objects.get(numero_serie = data['numero_serie'])
            #verificar que el dispositivo no tenga a ninguna usuaria asignada
            if registrado.usuaria:
                raise serializers.ValidationError('Numero de serie incorrecto')
        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Numero de serie incorrecto.')
        return(data)


    def create(self,data):
        dispositivo = DispositivoRastreador.objects.get(numero_serie=data['numero_serie'])
        dispositivo.estado = data['estado']
        dispositivo.pin_desactivador = data['pin_desactivador']
        persona = Persona.objects.get(email=data['email'])
        usuaria = Usuaria.objects.get(persona=persona)
        dispositivo.usuaria = usuaria 
        dispositivo.save()

        return dispositivo
"""

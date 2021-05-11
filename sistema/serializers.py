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
import datetime

#importando los modelos
from .models import *

#importando los modelos de catalogo
from catalogo.models import *

#Modelserializers del catalogo
from catalogo.serializers import *

#envio de correos
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

#expresiones regulares
import re

#envio de notificaciones con Firebase Cloud Messaging
from fcm_django.models import FCMDevice



"""Informacion de la persona"""
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

"""Serializer para el login de cualquier persona en el sistema"""
class personaLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(min_length=8)

    def validate(self,data):
        #saber si la persona o usuaria estan registrados
        persona = authenticate(username=data['email'],password=data['password'])
        
        if not persona:
            raise serializers.ValidationError('Credenciales invalidas.')

        self.context['persona'] = persona

        return data

    def create(self,data):
        #genera o devuelve el token de la persona (usuaria o contacto de confianza)
        token, created = Token.objects.get_or_create(user=self.context['persona'])
        return self.context['persona'], token.key

"""Serializer para el signup de una persona"""
class personaSignupSerializer(serializers.Serializer):
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

"""Serializer para cambiar el password de una persona"""
class cambiarPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8)

    def validate(self,data):

        #validar el password
        passwd = data['password']
        passwdConf = data['password_confirmation']

        #validar que el password nuevo sea igual
        if passwd != passwdConf:
            raise serializers.ValidationError('Los passwords ingresados debe de coincidir.')

        #validar que el password no sea muy comun
        password_validation.validate_password(passwd)

        return data

    def create(self,data):

        #instancia de la persona
        persona = Persona.objects.get(username=data['username'])

        #guardar el password nuevo
        persona.set_password(data['password'])
        persona.save()

        return persona

"""Serializer para enviar correo de recuperacion donde se cambia la contraseña"""
class personaRecuperarSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self,data):
        #validar que exista una cuenta asociada a este email
        try:
            Persona.objects.get(email=data['email'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('No existe ninguna cuenta asociada a este correo electronico.')
        return data

    def create(self,data):
        persona = Persona.objects.get(email=data['email'])
        #enviar el correo electronico para reestablecer la cuenta
        self.enviarEmail(persona)        
        return persona
        
    def enviarEmail(self,persona):
        #obtener el token de la persona para que pueda reestablecer su contraseña
        token = self.obtenerToken(persona)

        subject = 'Restablece tu contraseña'
        from_email = 'ProyectoTerminal03@gmail.com'
        
        content = render_to_string(
            'recuperarCuenta.html',
            {'token':token,'nombre':persona.nombre}
        )
        
        msg = EmailMultiAlternatives(subject, content, from_email, [persona.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def obtenerToken(self,persona):
        #obtener el token de la persona que solicita el cambio de password
        token, created = Token.objects.get_or_create(user=persona)
        return token.key

"""Serializer para restablecer la contraseña"""
class restablecerPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password  = serializers.CharField()
    password_confirmation = serializers.CharField()

    def validate(self,data):
        token = data['token']
        passwd = data['password']
        passwdConf = data['password_confirmation']

        #valida que las contraseñas sean iguales
        if passwd != passwdConf:
            raise serializers.ValidationError('Las claves ingresadas no coinciden')

        #validar que la contraseña no sea muy sencilla
        password_validation.validate_password(passwd)
        
        #validar que el token pertenezca a una persona valida
        try:
            user = Token.objects.get(key=token).user
        except:
            raise serializers.ValidationError('Informacion del usuario incorrecta')
        
        return data
    
    def create(self,data):
        #instancia de la persona
        persona = Token.objects.get(key=data['token']).user

        #guardar el password nuevo
        persona.set_password(data['password'])
        persona.save()

        return persona

"""Serializer para que una persona se convierta en usuaria"""
class convertirUsuariaSerializer(serializers.Serializer):
    #username de la persona
    username = serializers.CharField()
    
    #datos de la usuaria
    estatura = serializers.IntegerField()
    escolaridad = serializers.CharField(max_length=30)
    estado_civil = serializers.CharField()
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
        persona = Persona.objects.get(username=data['username'])

        #validar si ya existe la usuaria
        try:
            Usuaria.objects.get(persona = persona)
            raise serializers.ValidationError('Ya eres una usuaria.')
        except Usuaria.DoesNotExist:
            pass

        self.validarEdad(persona)
        self.validarGenero(persona)
        self.validarInformacion(data)
        self.validarEnfermedades(data)
        
        return data

    def validarEdad(self,persona):
        #obtener la edad de la persona
        edadDias = date.today() - persona.fecha_nacimiento
        edadPersona = edadDias.days // 365
        #saber si la persona cumple con el criterio de edad
        if edadPersona < 15:
            raise serializers.ValidationError('Debes de tener al menos 15 años.')

    def validarGenero(self,persona):
        #obtener el genero de la usuaria
        genero = persona.genero
        respuestaFemenino = re.compile(r'femenino',re.IGNORECASE)
        isFemenino = respuestaFemenino.search(genero)
        #saber si la persona cumple con el criterio de genero
        if isFemenino == None:
            raise serializers.ValidationError('Solo mujeres pueden ingresar a esta funcionalidad.')

    def validarInformacion(self,data):
        #validar que la informacion de la usuaria de las llaves foraneas exista
        try:
            EstadoCivil.objects.get(estado_civil = data['estado_civil'])
        except EstadoCivil.DoesNotExist:
            raise serializers.ValidationError('Este estado civil no se encuentra registrado.')
        
        try:
            Pais.objects.get(nacionalidad = data['nacionalidad'])
        except Pais.DoesNotExist:
            raise serializers.ValidationError('Esta nacionalidad no se encuentra disponible.')

        try:
            TipoNariz.objects.get(tipo_nariz=data['tipo_nariz'])
        except TipoNariz.DoesNotExist:
            raise serializers.ValidationError('Este tipo de nariz no se encuentra disponible.')

        try:
            Complexion.objects.get(complexion=data['complexion'])
        except Complexion.DoesNotExist:
            raise serializers.ValidationError('Este tipo de complexion no se encuentra disponible.')

        try:
            ColorOjos.objects.get(color_ojo=data['color_ojo'])
        except ColorOjos.DoesNotExist:
            raise serializers.ValidationError('Este color de ojos no se encuentra disponible.')

        try:
            FormaRostro.objects.get(forma_rostro=data['forma_rostro'])
        except FormaRostro.DoesNotExist:
            raise serializers.ValidationError('Esta forma de rostro no se encuentra disponible.')

        try:
            ColorCabello.objects.get(color_cabello=data['color_cabello'])
        except ColorCabello.DoesNotExist:
            raise serializers.ValidationError('Este color de cabello no se encuentra disponible.')

        try:
            ColorPiel.objects.get(color_piel=data['color_piel'])
        except ColorPiel.DoesNotExist:
            raise serializers.ValidationError('Este color de piel no se  encuentra disponible.')

        try:
            TipoCejas.objects.get(tipo_ceja=data['tipo_ceja'])
        except TipoCejas.DoesNotExist:
            raise serializers.ValidationError('Este tipo de cejas no se encuentra disponible.')

        try:
            TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])
        except TexturaCabello.DoesNotExist:
            raise serializers.ValidationError('Esta textura de cabello no se encuentra disponible.')
        
    def validarEnfermedades(self,data):
        #validar que las enfermedades existan en la base de datos
        enfermedades = data['enfermedades']
        numeroEnfermedades = len(enfermedades)

        for enfermedadData in enfermedades:
            try:
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
                #validar que no se registre "Ninguna" y otra enfermedad
                if enfermedadData['nombre_enfermedad'] == 'Ninguna' and numeroEnfermedades != 1:
                    raise serializers.ValidationError('No puedes registrar ninguna y otra enfermedad.')

            except Enfermedad.DoesNotExist:
                raise serializers.ValidationError('Esta enfermedad no se encuentra disponible.')

    def create(self,data):
        #instancia de la persona 
        persona = Persona.objects.get(username=data['username'])

        #isntancias de las llaves foraneas
        estado_civil = EstadoCivil.objects.get(estado_civil=data['estado_civil'])
        pais = Pais.objects.get(nacionalidad=data['nacionalidad'])
        tipo_nariz = TipoNariz.objects.get(tipo_nariz=data['tipo_nariz'])
        complexion = Complexion.objects.get(complexion=data['complexion'])
        color_ojo = ColorOjos.objects.get(color_ojo=data['color_ojo'])
        forma_rostro = FormaRostro.objects.get(forma_rostro=data['forma_rostro'])
        color_cabello = ColorCabello.objects.get(color_cabello=data['color_cabello'])
        color_piel = ColorPiel.objects.get(color_piel=data['color_piel'])
        tipo_ceja = TipoCejas.objects.get(tipo_ceja=data['tipo_ceja'])
        textura_cabello = TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])

        #modificar 'is_usuaria'
        persona.is_usuaria = True
        persona.save()

        #registro de la usuaria
        usuaria = Usuaria.objects.create(
            persona = persona,
            estatura = data['estatura'],
            escolaridad = data['escolaridad'],
            #llaves foraneas
            estado_civil = estado_civil,
            pais = pais,
            tipo_nariz = tipo_nariz,
            complexion = complexion,
            color_ojo = color_ojo,
            forma_rostro = forma_rostro,
            color_cabello = color_cabello,
            color_piel = color_piel,
            tipo_ceja = tipo_ceja,
            textura_cabello = textura_cabello
        )
        
        #guardar las enfermedades
        self.registrarEnfermedades(usuaria,data)

        return persona

    def registrarEnfermedades(self,usuaria,data):
        enfermedades = data.pop('enfermedades')
        for enfermedadData in enfermedades:
            usuaria.enfermedades.add(
                #objeto de la enfermedad
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
            )
        usuaria.save()




"""Serializer para que una usuaria que se regustra dentro del sistema"""
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
    estado_civil = serializers.CharField()
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
        
        passwd = data['password']
        passwdConf = data['password_confirmation']
        genero = data['genero']
        
        #validar las contraseñas, deben ser iguales
        if passwd != passwdConf:
            raise serializers.ValidationError('Las contraseñas ingresadas no coinciden.')
        
        #valida que la contraseña no sea comun
        password_validation.validate_password(passwd)

        #validar la edad de la usuaria
        self.validarEdad(data)
        #validar el genero de la usuaria
        self.validarGenero(data)
        #validar que los datos existan dentro de la base de datos
        self.validarInformacion(data)
        #validar las enfermedades de la usuaria
        self.validarEnfermedades(data)

        return(data)

    def validarEdad(self,data):
        hoy = date.today()
        fecha_nacimiento = data['fecha_nacimiento']
        edadDias = hoy - fecha_nacimiento
        
        if edadDias.days < 5475:
            raise serializers.ValidationError('Debes de tener al menos 15 años.')

    def validarGenero(self,data):
        #obtener el genero de la usuaria
        genero = data['genero']
        respuestaFemenino = re.compile(r'femenino',re.IGNORECASE)
        isFemenino = respuestaFemenino.search(genero)
        #saber si la persona cumple con el criterio de genero
        if isFemenino == None:
            raise serializers.ValidationError('Solo mujeres pueden ingresar a esta funcionalidad.')
    
    def validarInformacion(self,data):
        #validar que la informacion de la usuaria de las llaves foraneas exista
        try:
            EstadoCivil.objects.get(estado_civil = data['estado_civil'])
        except EstadoCivil.DoesNotExist:
            raise serializers.ValidationError('Este estado civil no se encuentra registrado.')
        
        try:
            Pais.objects.get(nacionalidad = data['nacionalidad'])
        except Pais.DoesNotExist:
            raise serializers.ValidationError('Esta nacionalidad no se encuentra disponible.')

        try:
            TipoNariz.objects.get(tipo_nariz=data['tipo_nariz'])
        except TipoNariz.DoesNotExist:
            raise serializers.ValidationError('Este tipo de nariz no se encuentra disponible.')

        try:
            Complexion.objects.get(complexion=data['complexion'])
        except Complexion.DoesNotExist:
            raise serializers.ValidationError('Este tipo de complexion no se encuentra disponible.')

        try:
            ColorOjos.objects.get(color_ojo=data['color_ojo'])
        except ColorOjos.DoesNotExist:
            raise serializers.ValidationError('Este color de ojos no se encuentra disponible.')

        try:
            FormaRostro.objects.get(forma_rostro=data['forma_rostro'])
        except FormaRostro.DoesNotExist:
            raise serializers.ValidationError('Esta forma de rostro no se encuentra disponible.')

        try:
            ColorCabello.objects.get(color_cabello=data['color_cabello'])
        except ColorCabello.DoesNotExist:
            raise serializers.ValidationError('Este color de cabello no se encuentra disponible.')

        try:
            ColorPiel.objects.get(color_piel=data['color_piel'])
        except ColorPiel.DoesNotExist:
            raise serializers.ValidationError('Este color de piel no se  encuentra disponible.')

        try:
            TipoCejas.objects.get(tipo_ceja=data['tipo_ceja'])
        except TipoCejas.DoesNotExist:
            raise serializers.ValidationError('Este tipo de cejas no se encuentra disponible.')

        try:
            TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])
        except TexturaCabello.DoesNotExist:
            raise serializers.ValidationError('Esta textura de cabello no se encuentra disponible.')
        
    def validarEnfermedades(self,data):
        #validar que las enfermedades existan en la base de datos
        enfermedades = data['enfermedades']
        numeroEnfermedades = len(enfermedades)

        for enfermedadData in enfermedades:
            try:
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
                #validar que no se registre "Ninguna" y otra enfermedad
                if enfermedadData['nombre_enfermedad'] == 'Ninguna' and numeroEnfermedades != 1:
                    raise serializers.ValidationError('No puedes registrar ninguna y otra enfermedad.')

            except Enfermedad.DoesNotExist:
                raise serializers.ValidationError('Esta enfermedad no se encuentra disponible.')

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

        #registro de la usuaria
        usuaria = Usuaria.objects.create(
            #instancia de la persona
            persona = persona,
            #datos de la usuaria
            estatura=data['estatura'],
            escolaridad=data['escolaridad'],
            #llaves foraneas de la usuaria
            estado_civil=EstadoCivil.objects.get(estado_civil=data['estado_civil']),
            pais=Pais.objects.get(nacionalidad=data['nacionalidad']),
            tipo_nariz=TipoNariz.objects.get(tipo_nariz=data['tipo_nariz']),
            complexion=Complexion.objects.get(complexion=data['complexion']),
            color_ojo=ColorOjos.objects.get(color_ojo=data['color_ojo']),
            forma_rostro=FormaRostro.objects.get(forma_rostro=data['forma_rostro']),
            color_cabello=ColorCabello.objects.get(color_cabello=data['color_cabello']),
            color_piel=ColorPiel.objects.get(color_piel=data['color_piel']),
            tipo_ceja=TipoCejas.objects.get(tipo_ceja=data['tipo_ceja']),
            textura_cabello=TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])
        )

        #registro de las enfermedades
        self.registrarEnfermedades(usuaria,data)
        
        #obtener el token
        self.context['persona'] = persona
        token, created = Token.objects.get_or_create(user=self.context['persona'])
        return persona, token.key

    def registrarEnfermedades(self,usuaria,data):
        #registro de la o las enfermedades que padece la usuaria
        enfermedades = data.pop('enfermedades')
        for enfermedadData in enfermedades:
            usuaria.enfermedades.add(
                #objeto de la enfermedad
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
            )
        usuaria.save()

"""Informacion de la usuaria"""
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
    estado_civil = EstadoCivilSerializer()
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

"""Serializer para actualizar la informacion de una usuaria"""
class usuariaActualizarSerializer(serializers.Serializer):
    username = serializers.CharField()
    estatura = serializers.IntegerField()
    escolaridad = serializers.CharField(max_length=30)

    estado_civil = serializers.CharField(max_length=30) 
    nacionalidad = serializers.CharField(max_length=30)
    tipo_nariz = serializers.CharField(max_length=30)
    complexion = serializers.CharField(max_length=20)
    color_ojo = serializers.CharField(max_length=20)
    forma_rostro = serializers.CharField(max_length=30)
    color_cabello = serializers.CharField(max_length=20) 
    color_piel = serializers.CharField(max_length=30)
    tipo_ceja = serializers.CharField(max_length=15)
    textura_cabello = serializers.CharField(max_length=30)

    enfermedades = EnfermedadSerializer(many=True)

    def validate(self,data):
        #validar que exista cada una de las opciones
        self.validarInformacion(data)
        #validar que las enfermedades existan 
        self.validarEnfermedades(data)

        return data

    def validarInformacion(self,data):
        try:
            EstadoCivil.objects.get(estado_civil=data['estado_civil'])
        except EstadoCivil.DoesNotExist:
            raise serializers.ValidationError('Este estado civil no es valido')

        try:
            Pais.objects.get(nacionalidad=data['nacionalidad'])
        except Pais.DoesNotExist:
            raise serializers.ValidationError('Este pais no es valido')

        try:
            TipoNariz.objects.get(tipo_nariz=data['tipo_nariz'])
        except TipoNariz.DoesNotExist:
            raise serializers.ValidationError('Este tipo de nariz no es valido')

        try:
            Complexion.objects.get(complexion=data['complexion'])
        except Complexion.DoesNotExist:
            raise serializers.ValidationError('Esta complexion no es valida')

        try:
            ColorOjos.objects.get(color_ojo=data['color_ojo'])
        except ColorOjos.DoesNotExist:
            raise serializers.ValidationError('Este color de ojos no es valido')

        try:
            FormaRostro.objects.get(forma_rostro=data['forma_rostro'])
        except FormaRostro.DoesNotExist:
            raise serializers.ValidationError('Esta forma de rostro no es valida')

        try:
            ColorCabello.objects.get(color_cabello=data['color_cabello'])
        except ColorCabello.DoesNotExist:
            raise serializers.ValidationError('Este color de cabello no es valido')

        try:
            ColorPiel.objects.get(color_piel=data['color_piel'])
        except ColorPiel.DoesNotExist:
            raise serializers.ValidationError('Este color de piel no es valido')

        try:
            TipoCejas.objects.get(tipo_ceja=data['tipo_ceja'])
        except TipoCejas.DoesNotExist:
            raise serializers.ValidationError('Este tipo de ceja no es valido')

        try:
            TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])
        except TexturaCabello.DoesNotExist:
            raise serializers.ValidationError('Esta textura de cabello no es valida')

    def validarEnfermedades(self,data):
        #validar que las enfermedades existan en la base de datos
        enfermedades = data['enfermedades']
        numeroEnfermedades = len(enfermedades)

        for enfermedadData in enfermedades:
            try:
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
                #validar que no se registre "Ninguna" y otra enfermedad
                if enfermedadData['nombre_enfermedad'] == 'Ninguna' and numeroEnfermedades != 1:
                    raise serializers.ValidationError('No puedes registrar ninguna y otra enfermedad.')

            except Enfermedad.DoesNotExist:
                raise serializers.ValidationError('Esta enfermedad no se encuentra disponible.')

    def create(self,data):
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #instancias que se tienen que guardar
        estado_civil = EstadoCivil.objects.get(estado_civil=data['estado_civil'])
        pais = Pais.objects.get(nacionalidad=data['nacionalidad'])
        tipo_nariz = TipoNariz.objects.get(tipo_nariz=data['tipo_nariz'])
        complexion = Complexion.objects.get(complexion=data['complexion'])
        color_ojo = ColorOjos.objects.get(color_ojo=data['color_ojo'])
        forma_rostro = FormaRostro.objects.get(forma_rostro=data['forma_rostro'])
        color_cabello = ColorCabello.objects.get(color_cabello=data['color_cabello'])
        color_piel = ColorPiel.objects.get(color_piel=data['color_piel'])
        tipo_ceja = TipoCejas.objects.get(tipo_ceja=data['tipo_ceja'])
        textura_cabello = TexturaCabello.objects.get(textura_cabello=data['textura_cabello'])

        #salvar los datos nuevos
        usuaria.estatura = data['estatura']
        usuaria.escolaridad = data['escolaridad']
        usuaria.estado_civil = estado_civil
        usuaria.pais = pais
        usuaria.tipo_nariz = tipo_nariz
        usuaria.complexion = complexion
        usuaria.color_ojo = color_ojo
        usuaria.forma_rostro = forma_rostro
        usuaria.color_cabello = color_cabello
        usuaria.color_piel = color_piel
        usuaria.tipo_ceja = tipo_ceja
        usuaria.textura_cabello = textura_cabello

        #guardar las enfermedades
        enfermedades = data.pop('enfermedades')
        for enfermedadData in enfermedades:
            usuaria.enfermedades.add(
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
            )

        #remover Ninguna si es el caso
        queryset = usuaria.enfermedades.filter(nombre_enfermedad='Ninguna') 
        if queryset:
            #remover Ninguna
            ninguna = Enfermedad.objects.get(nombre_enfermedad='Ninguna')
            usuaria.enfermedades.remove(ninguna)

        usuaria.save()

        return usuaria

"""Serializer para borrar una enfermedad"""
class usuariaEnfermedadSerializer(serializers.Serializer):
    username = serializers.CharField()
    nombre_enfermedad = serializers.CharField(max_length=30)

    def validate(self,data):
        #validar que la enfermedad que se va a borrar exista
        try:
            Enfermedad.objects.get(nombre_enfermedad=data['nombre_enfermedad'])
        except Enfermedad.DoesNotExist:
            raise serializers.ValidationError('Esta enfermedad no existe')
            
        #validar que el nombre de la enfermedad no sea ninguno 
        if data['nombre_enfermedad'] == 'Ninguna':
            raise serializers.ValidationError('Informacion incorrecta')

        return data

    def create(self,data):
        
        #isntancia de la usuaria
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #Contar el total de enfermedades que padece una usuaria
        if usuaria.enfermedades.all().count() == 1:
            #agregar registro de ninguno como enfermedad
            enfermedad = Enfermedad.objects.get(nombre_enfermedad='Ninguna')
            usuaria.enfermedades.add(enfermedad)

            #isntancia que se va a remover
            remover = Enfermedad.objects.get(nombre_enfermedad=data['nombre_enfermedad'])
            usuaria.enfermedades.remove(remover)
            usuaria.save()
        
        else:
            #isntancia que se va a remover
            remover = Enfermedad.objects.get(nombre_enfermedad=data['nombre_enfermedad'])
            usuaria.enfermedades.remove(remover)
            usuaria.save()
        
        return usuaria




"""Serializer para ver informacion basica de un dispositivo"""
class dispositivoInformacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispositivoRastreador
        fields = (
            'numero_serie',
            'pin_desactivador'
        )

"""Serializer para asociar a una usuaria con un dispositivo"""
class dispositivoAsociarSerializer(serializers.Serializer):
    username = serializers.CharField()
    numero_serie = serializers.IntegerField()
    pin_desactivador = serializers.IntegerField()


    def validate(self,data):

        #buscar si el dispositivo se encuentra dentro de la base de datos
        try:
            dispositivo = DispositivoRastreador.objects.get(numero_serie = data['numero_serie'])
            #verificar que el dispositivo no tenga a ninguna usuaria asignada
            if dispositivo.usuaria:
                raise serializers.ValidationError('Numero de serie incorrecto.')
        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Numero de serie incorrecto.')

        return data

    def create(self,data):
        #instancia de la usuaria
        persona = Persona.objects.get(username =data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #instancia del dispositivo rastreador
        dispositivo = DispositivoRastreador.objects.get(numero_serie = data['numero_serie'])

        #modificar el registro del dispositivo
        dispositivo.usuaria = usuaria
        dispositivo.pin_desactivador = data['pin_desactivador']
        dispositivo.save()

        return dispositivo

"""Serializer para desasociar el dispositivo de una usuaria"""
class dispositivoDesasociarSerializer(serializers.Serializer):
    username = serializers.CharField()
    numero_serie = serializers.IntegerField()

    def validate(self, data):
        #saber si la usuaria existe
        try:
            persona = Persona.objects.get(username =data['username'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username invalido.')

        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Username invalido.')

        #encontrar si la usuaria tiene este dispositivo asociado
        try:
            dispositivo = DispositivoRastreador.objects.get(
                numero_serie = data['numero_serie'],
                usuaria= usuaria
            )
        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Este dispositivo no existe, verifica tu informacion.')

        return data

    def create(self,data):
        #instancia de la usuaria
        persona = Persona.objects.get(username =data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #dispositivo
        dispositivo = DispositivoRastreador.objects.get(
            numero_serie = data['numero_serie'],
            usuaria = usuaria
        )

        dispositivo.pin_desactivador = None
        dispositivo.usuaria = None

        dispositivo.save()

        return dispositivo

"""Serializer para cambiar el pin desactivador del dispositivo de una usuaria"""
class dispositivoPinSerializer(serializers.Serializer):
    username = serializers.CharField()
    numero_serie = serializers.IntegerField()
    pin_desactivador = serializers.IntegerField()

    def validate(self,data):
        #comprobar si existe la usuaria
        try:
            persona = Persona.objects.get(username =data['username'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username incorrecto.')
        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Username incorrecto.')

        #encontrar el dispositivo
        try:
            DispositivoRastreador.objects.get(
                numero_serie=data['numero_serie'],
                usuaria = usuaria
            )
        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Numero de serie incorrecto.')

        return data

    def create(self,data):
        #instancia de la usuaria
        persona = Persona.objects.get(username =data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #dispositivo de la usuaria
        dispositivo = DispositivoRastreador.objects.get(
            numero_serie=data['numero_serie'],
            usuaria = usuaria
        )

        dispositivo.pin_desactivador = data['pin_desactivador']
        dispositivo.save()

        return dispositivo




"""Informacion del grupo de confianza (nombre y clave de acceso)"""
class grupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grupo
        fields = (
            'nombre',
            'clave_acceso'
        )

"""Creacion del grupo de confianza"""
class grupoCrearSerializer(serializers.Serializer):
    #validar el tamaño del nombre del grupo
    username = serializers.CharField()
    nombre = serializers.CharField(max_length=20)

    def validate(self,data):

        #verificar que no se haya excedido el maximo numero de grupo permitidos
        grupos = Grupo.objects.all().count()
        if grupos == 1000000:
            raise serializers.ValidationError('Ya no existen grupos disponibles.')

        #verificar que la usuaria no tenga un grupo
        try:
            persona = Persona.objects.get(username =data['username'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username invalido.')

        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Usuario invalido.')

        try:
            grupo = Grupo.objects.get(usuaria=usuaria)
            raise serializers.ValidationError('Ya tienes un grupo de confianza.')
        except Grupo.DoesNotExist:
            pass

        #validar la clave de acceso
        self.validarClave()

        return(data)

    def validarClave(self):
        #validar la clave de acceso no este en uso por otro grupo
        seed(1)
        while True:
            clave = "%06d" % randint(0,999999)
            try:
                Grupo.objects.get(clave_acceso=clave)
            except Grupo.DoesNotExist:
                self.context['clave'] = clave
                break

    def create(self,data):
        #obtener a la usuaria
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #guardar la informacion
        data.pop('username')
        grupo = Grupo.objects.create(
            **data,
            usuaria = usuaria,
            clave_acceso = self.context['clave']
        )

        return grupo

"""Informacion de los miembros del grupo"""
class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            'username',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
        )

"""Informacion bascia del grupo de confianza, solo lo puede visualizar la usuaria"""
class grupoInformacionSerializer(serializers.ModelSerializer):
    integrantes = MiembroSerializer(many=True)

    class Meta:
        model = Grupo
        fields = (
            'nombre',
            'clave_acceso',
            'integrantes',
        )

"""Unirse al grupo de confianza"""
class grupoUnirSerializer(serializers.Serializer):

    username = serializers.CharField()
    clave_acceso = serializers.CharField()

    def validate(self,data):
        #validar que el grupo al que se quiere unir exista
        try:
            grupo = Grupo.objects.get(clave_acceso = data['clave_acceso'])
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('Verifica tu clave de acceso.')

        #validar el limite de usuarios dentro del grupo
        totalMiembros = grupo.integrantes.all().count()
        if totalMiembros == 5:
            raise serializers.ValidationError('No se pueden agregar mas miembros a este grupo.')

        #validar que no se vuelva a unir a un grupo esta persona
        persona = Persona.objects.get(username=data['username'])

        try:
            Miembros.objects.get(grupo=grupo, persona=persona)
            raise serializers.ValidationError('Ya formas parte de este grupo de confianza.')
        except Miembros.DoesNotExist:
            pass

        return data

    def create(self,data):

        grupo = Grupo.objects.get(clave_acceso=data['clave_acceso'])
        persona = Persona.objects.get(username =data['username'])

        miembro = Miembros.objects.create(
            grupo=grupo,
            persona=persona,
            fecha_union=datetime.date.today()
        )

        return grupo

"""Informacion que puede visualizar el contacto de confianza sobre el grupo al momento de unirse"""
class grupoInformacionPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ('nombre',)

"""Serializer para expulsar a una persona de un grupo de confianza"""
class grupoExpulsarSerializer(serializers.Serializer):
    username_usuaria = serializers.CharField()
    username_persona = serializers.CharField()

    def validate(self, data):

        #saber si la usuaria tiene un grupo de confianza
        try:
            grupo = Grupo.objects.get(usuaria__persona__username=data['username_usuaria'])
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('Informacion de la usuaria incorrecta.')

        #saber si el contacto de confianza existe
        try:
            contacto = Persona.objects.get(username =data['username_persona'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Informacion del miembro incorrecta.')

        #saber si en este grupo tiene a el miembro
        try:
            Miembros.objects.get(grupo=grupo ,persona= contacto)
        except Miembros.DoesNotExist:
            raise serializers.ValidationError('Este miembro no forma parte de tu grupo.')

        return data

    def create(self,data):
        #instancia del grupo
        grupo = Grupo.objects.get(usuaria__persona__username=data['username_usuaria'])

        #instancia de la persona que se va a expulsar
        miembro = Persona.objects.get(username =data['username_persona'])

        #removiendo al miembro
        miembro = Miembros.objects.get(grupo=grupo,persona=miembro)
        miembro.delete()

        return grupo

"""Serializer para cambiar el nombre de un grupo"""
class grupoNombreSerializer(serializers.Serializer):
    username = serializers.CharField()
    nombre = serializers.CharField(max_length=20)

    def validate(self,data):
        #verificar que el grupo exista
        try:
            grupo = Grupo.objects.get(usuaria__persona__username=data['username'])
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('Informacion del grupo incorrecta.')

        #verificar que el nombre nuevo del grupo sea diferente
        if grupo.nombre == data['nombre']:
            raise serializers.ValidationError('El nuevo nombre debe de ser diferente')

        return data

    def create(self,data):
        #instancia del grupo
        grupo = Grupo.objects.get(usuaria__persona__username = data['username'])

        #nuevo nombre del grupo asignado por la usuaria
        grupo.nombre = data['nombre']
        grupo.save()

        return grupo

"""Serializer para que el contacto vea informacion basica de la usuaria """
class personaInformacionBasicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            'username',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
        )

"""Serializer para que el contacto vea informacion basica de la usuaria"""
class usuariaGrupoSerializer(serializers.ModelSerializer):
    persona = personaInformacionBasicaSerializer()
    class Meta:
        model = Usuaria
        fields = (
            'persona',
        )

"""Serializer para ver los grupos a los que una persona pertenece"""
class misGruposSerializer(serializers.ModelSerializer):
    usuaria = usuariaGrupoSerializer()
    class Meta:
        model = Grupo
        fields = (
            'usuaria',
            'nombre',
        )




"""Serializer para publicar una alerta desde el dispositivo"""
class alertaPublicarSerializer(serializers.Serializer):
    numero_serie = serializers.IntegerField()
    nombre_alerta = serializers.CharField(max_length=30)
    latitud = serializers.DecimalField(max_digits=8, decimal_places=6)
    longitud = serializers.DecimalField(max_digits=9, decimal_places=6)
    fecha_hora = serializers.DateTimeField()
    fecha_hora_inicio = serializers.DateTimeField()

    def validate(self,data):
        #validar que el dipositivo exista
        try:
            dispositivo = DispositivoRastreador.objects.get(numero_serie = data['numero_serie'])
            #saber si el dispositivo tiene a una usuaria registrada
            if not dispositivo.usuaria:
                raise serializers.ValidationError('Numero de serie incorrecto')

        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Numero de serie incorrecto')

        return data

    def create(self,data):

        #dispositivo
        dispositivo = DispositivoRastreador.objects.get(numero_serie = data['numero_serie'])
        usuaria = dispositivo.usuaria

        #Grupo que administra la usuaria
        grupo = Grupo.objects.get(usuaria=usuaria)

        #Activar la alerta dentro del grupo
        grupo.estado_alerta = True
        grupo.save()

        #crear la instancia de la alerta, si ya existe devolver la instancia
        obj, created = Alerta.objects.get_or_create(
            grupo=grupo,
            nombre_alerta=data['nombre_alerta'],
            fecha_hora=data['fecha_hora_inicio']
        )

        #salvar la ubicacion de la alerta
        ubicacion = Ubicacion.objects.create(
            alerta= obj,
            latitud= data['latitud'],
            longitud= data['longitud'],
            fecha_hora= data['fecha_hora'],
        )
        ubicacion.save()

        #enviar notificacion si la alerta se registra por primera vez
        if created == True:
            self.enviarNotificacion(grupo,obj)

        return ubicacion

    def enviarNotificacion(self,grupo,alerta):
        #informacion del grupo
        nombre_grupo = grupo.nombre

        #informacion de la usuaria
        nombre = grupo.usuaria.persona.nombre
        apellido_paterno = grupo.usuaria.persona.apellido_paterno

        #informacion de la alerta
        nombre_alerta = alerta.nombre_alerta
        fecha_hora = alerta.fecha_hora

        integrantes = grupo.integrantes.all()
        for persona in integrantes:
            #nombre de la persona
            nombre_contacto = persona.nombre

            devices = FCMDevice.objects.filter(user=persona)
            devices.send_message(
                title='Hola {}, {} {} activo una alerta en el grupo "{}"'.format(
                    nombre_contacto,nombre,apellido_paterno,nombre_grupo
                ),
                body='La alerta de nombre: "{}" se registro a las {}'.format(
                    nombre_alerta,fecha_hora
                ),
                #duracion de 72 horas
                time_to_live=259200
            )

"""Serializer para que el dispositivo revise si la alerta fue desactivada"""
class grupoDesactivacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grupo
        fields = (
            'estado_alerta',
        )

"""Serializer para devolver las alertas activas de cada grupo en el que este una persona"""
class alertaGrupoSerializer(serializers.ModelSerializer):
    grupo = misGruposSerializer()

    class Meta:
        model = Alerta
        fields = (
            'grupo',
            'nombre_alerta',
            'fecha_hora',
        )

"""Serializer para devolver la trayectoria de una alerta"""
class trayectoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ubicacion
        fields = (
            'latitud',
            'longitud',
            'fecha_hora',
        )

"""Informacion que visualiza la usuaria de su alerta mas reciente"""
class alertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields=(
            'nombre_alerta',
            'fecha_hora',
        )

"""Serializer desactivar la alerta"""
class desactivarAlertaSerializer(serializers.Serializer):
    username = serializers.CharField()
    nombre_alerta= serializers.CharField(max_length=30)
    pin_desactivador=serializers.IntegerField()

    def validate(self,data):

        #validar informacion de la alerta
        self.validarAlerta(data)

        #validar el pin desactivador
        dispositivo = DispositivoRastreador.objects.filter(
            usuaria__persona__username=data['username'],
            pin_desactivador=data['pin_desactivador']
        )
        if not dispositivo:
            raise serializers.ValidationError('Pin incorrecto.')

        return data

    def validarAlerta(self,data):
        #validar que el grupo exista y tenga una la alerta activa
        try:
            grupo = Grupo.objects.get(usuaria__persona__username=data['username'],estado_alerta=True)
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('Este grupo no tiene ninguna alerta activa.')

        #validar que la alerta exista
        try:
            Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Esta alerta no existe.')
        
    def create(self,data):
        #instancia del grupo
        grupo = Grupo.objects.get(usuaria__persona__username=data['username'],estado_alerta=True)
        #instancia de la alerta
        alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])

        #desactivar alerta del grupo
        grupo.estado_alerta=False
        grupo.save()

        #enviar la notificacion de desactivacion
        self.enviarNotificacion(grupo,alerta)
        
        #borrar la alerta
        alerta.delete()

        return grupo
   
    def enviarNotificacion(self,grupo,alerta):
        #nombre de la usuaria
        nombre_usuaria = grupo.usuaria.persona.nombre
        apellido_paterno = grupo.usuaria.persona.apellido_paterno

        #nombre de la alerta
        nombre_alerta = alerta.nombre_alerta

        integrantes = grupo.integrantes.all()
        for persona in integrantes:
            nombre_contacto = persona.nombre
            devices = FCMDevice.objects.filter(user=persona)
            devices.send_message(
                title='Alerta desactivada',
                body='Hola {}, la alerta de nombre: "{}" fue desactivada por la usuaria {} {}'.format(
                    nombre_contacto,
                    nombre_alerta,
                    nombre_usuaria,
                    apellido_paterno
                ),
                time_to_live=259200
            ) 




"""Serializer para que el usuario vea informacion de la alerta dentro del cuestionario"""
class alertaCuestionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alerta
        fields = (
            'nombre_alerta',
            'fecha_hora',
        )

"""Serializer del cuestionario"""
class cuestionarioSerializer(serializers.ModelSerializer):
    alerta = alertaCuestionarioSerializer()
    circunstancia = CircunstanciaSerializer()
    lazo = LazoSerializer()

    class Meta:
        model = Cuestionario
        fields = (
            'alerta',
            'descripcion',
            'autoridad_denuncia',
            'modelo_vehiculo',
            'violencia',
            'acompanar',
            'denuncia_previa',
            'manejaba_auto',
            'estado_usuaria',
            'circunstancia',
            'lazo',
        )

"""Serializer para contestar cuestionarios"""
class cuestionarioCrearSerializer(serializers.Serializer):
    username_usuaria = serializers.CharField()
    username_persona = serializers.CharField()
    nombre_alerta = serializers.CharField(max_length=30)

    #datos del cuestionario
    descripcion = serializers.CharField(max_length=2000,allow_blank=True)
    autoridad_denuncia = serializers.CharField(max_length=50,allow_blank=True)
    modelo_vehiculo = serializers.CharField(max_length=50,allow_blank=True)
    violencia = serializers.CharField(max_length=2,allow_blank=True)
    acompanar = serializers.CharField(max_length=2,allow_blank=True)
    denuncia_previa = serializers.CharField(max_length=2,allow_blank=True)
    manejaba_auto = serializers.CharField(max_length=2,allow_blank=True)
    estado_usuaria = serializers.CharField(max_length=15)

    tipo_circunstancia = serializers.CharField(max_length=100)
    lazo = serializers.CharField(max_length=30)

    def validate(self,data):

        #validar circunstancia y lazo
        self.validarInformacion(data)
        
        #instancia del grupo
        try:
            grupo = Grupo.objects.get(
                usuaria__persona__username=data['username_usuaria'],
                estado_alerta=True
            )
        except:
            raise serializers.ValidationError('Informacion del grupo incorrecta.')

        #saber si existe una alerta con este nombre
        #saber si la alerta forma parte de este grupo
        try:
            alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Informacion de la alerta incorrecta.')

        #saber si la persona es miembro de este grupo
        try:
            persona = Persona.objects.get(username=data['username_persona'])
            miembro = Miembros.objects.get(grupo=grupo,persona=persona)
        except:
            raise serializers.ValidationError('Esta persona no es miembro del grupo.')

        #saber si el miembro no ha contestado previamente esa alerta
        try:
            Cuestionario.objects.get(alerta=alerta,miembro=miembro)
            raise serializers.ValidationError('Ya respondiste este cuestionario.')
        except Cuestionario.DoesNotExist:
            pass

        return data

    def validarInformacion(self,data):
        #saber si existe el tipo de circunstancia
        try:
            Circunstancia.objects.get(tipo_circunstancia=data['tipo_circunstancia'])
        except Circunstancia.DoesNotExist:
            raise serializers.ValidationError('Este tipo de circunstancia no se encuentra registrada')

        #saber si existe el lazo
        try:
            Lazo.objects.get(lazo=data['lazo'])
        except Lazo.DoesNotExist:
            raise serializers.ValidationError('Este lazo no se encuentra registrado')

    def create(self,data):

        #instancia del tipo de circunstancia
        circunstancia = Circunstancia.objects.get(tipo_circunstancia=data['tipo_circunstancia'])

        #instancia del lazo
        lazo = Lazo.objects.get(lazo=data['lazo'])

        #instancia del grupo
        grupo = Grupo.objects.get(usuaria__persona__username=data['username_usuaria'])

        #instancia de la alerta
        alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])

        #instancia del miembro
        persona = Persona.objects.get(username=data['username_persona'])
        miembro = Miembros.objects.get(persona=persona,grupo=grupo)

        data.pop('username_usuaria')
        data.pop('username_persona')
        data.pop('nombre_alerta')
        data.pop('tipo_circunstancia')
        data.pop('lazo')

        #creacion del cuestionario
        cuestionario = Cuestionario.objects.create(
            miembro=miembro,
            alerta=alerta,
            **data,
            circunstancia=circunstancia,
            lazo=lazo
        )

        return cuestionario

"""Serializer para actualizar el cuestionario"""
class cuestionarioActualizarSerializer(serializers.Serializer):
    username_usuaria = serializers.CharField()
    username_persona = serializers.CharField()
    nombre_alerta = serializers.CharField(max_length=30)

    #datos del cuestionario
    descripcion = serializers.CharField(max_length=2000,allow_blank=True)
    autoridad_denuncia = serializers.CharField(max_length=50,allow_blank=True)
    modelo_vehiculo = serializers.CharField(max_length=50,allow_blank=True)
    violencia = serializers.CharField(max_length=2,allow_blank=True)
    acompanar = serializers.CharField(max_length=2,allow_blank=True)
    denuncia_previa = serializers.CharField(max_length=2,allow_blank=True)
    manejaba_auto = serializers.CharField(max_length=2,allow_blank=True)
    estado_usuaria = serializers.CharField(max_length=15)

    #datos del cuestionario que son llaves foraneas
    tipo_circunstancia = serializers.CharField(max_length=100)
    lazo = serializers.CharField(max_length=30)

    def validate(self,data):

        #saber si el grupo existe
        #saber si el grupo tiene una alerta activa
        try:
            grupo = Grupo.objects.get(
                usuaria__persona__username=data['username_usuaria'],
                estado_alerta=True
            )
        except:
            raise serializers.ValidationError('Informacion del grupo incorrecta.')

        #saber si existe una alerta con este nombre
        #saber si la alerta forma parte de este grupo
        try:
            alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Informacion de la alerta incorrecta.')

        #saber si la persona es miembro de este grupo
        try:
            persona = Persona.objects.get(username=data['username_persona'])
            miembro = Miembros.objects.get(grupo=grupo,persona=persona)
        except:
            raise serializers.ValidationError('Esta persona no es miembro del grupo.')

        #saber si ya ha contestado el cuestionario
        try:
            Cuestionario.objects.get(alerta=alerta,miembro=miembro)
        except Cuestionario.DoesNotExist:
            raise serializers.ValidationError('Aun no haz contestado el cuestionario.')

        return data

    def validarInformacion(self,data):
        #saber si existe el tipo de circunstancia
        try:
            Circunstancia.objects.get(tipo_circunstancia=data['tipo_circunstancia'])
        except Circunstancia.DoesNotExist:
            raise serializers.ValidationError('Este tipo de circunstancia no se encuentra registrada.')

        #saber si existe el lazo
        try:
            Lazo.objects.get(lazo=data['lazo'])
        except Lazo.DoesNotExist:
            raise serializers.ValidationError('Este lazo no se encuentra registrado.')

    def create(self,data):
        #instancia de la circunstancia
        circunstancia = Circunstancia.objects.get(tipo_circunstancia=data['tipo_circunstancia'])

        #instacia del lazo
        lazo = Lazo.objects.get(lazo=data['lazo'])

        #grupo de la usuaria
        admin = Persona.objects.get(username=data['username_usuaria'])
        usuaria = Usuaria.objects.get(persona=admin)
        grupo = Grupo.objects.get(usuaria=usuaria)

        #instancia de la alerta
        alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])

        #instancia del miembro
        persona = Persona.objects.get(username=data['username_persona'])
        miembro = Miembros.objects.get(persona=persona,grupo=grupo)

        #instancia del cuestionario
        cuestionario = Cuestionario.objects.get(alerta=alerta,miembro=miembro)

        #modificar datos de este cuestionario
        cuestionario.descripcion = data['descripcion']
        cuestionario.autoridad_denuncia =data['autoridad_denuncia']
        cuestionario.modelo_vehiculo =data['modelo_vehiculo']
        cuestionario.violencia =data['violencia']
        cuestionario.acompanar =data['acompanar']
        cuestionario.denuncia_previa =data['denuncia_previa']
        cuestionario.manejaba_auto =data['manejaba_auto']
        cuestionario.estado_usuaria =data['estado_usuaria']

        cuestionario.circunstancia = circunstancia
        cuestionario.lazo = lazo
        cuestionario.save()

        return cuestionario

"""Serializer para traer el cuestionario llenado por un miembro"""
class miCuestionarioSerializer(serializers.Serializer):

    username_usuaria = serializers.CharField()
    username_persona = serializers.CharField()
    nombre_alerta = serializers.CharField()

    def validate(self,data):

        #encontrar el grupo de la usuaria
        try:
            grupo = Grupo.objects.get(usuaria__persona__username=data['username_usuaria'])
        except:
            raise serializers.ValidationError('Informacion del grupo invalida.')

        #encontrar la alerta
        try:
            alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Informacion de la alerta invalida.')

        #encontrar el miembro
        try:
            persona = Persona.objects.get(username=data['username_persona'])
            miembro = Miembros.objects.get(grupo=grupo,persona=persona)
        except:
            raise serializers.ValidationError('No eres parte de este grupo.')

        #encontrar el cuestionario
        try:
            cuestionario = Cuestionario.objects.get(miembro=miembro,alerta=alerta)
        except Cuestionario.DoesNotExist:
            raise serializers.ValidationError('Aun no haz respondido el cuestionario.')

        return data

    def create(self,data):

        #grupo
        grupo = Grupo.objects.get(usuaria__persona__username=data['username_usuaria'])

        #alerta
        alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])

        #miembro
        persona = Persona.objects.get(username=data['username_persona'])
        miembro = Miembros.objects.get(persona=persona,grupo=grupo)

        #cuestionario
        cuestionario = Cuestionario.objects.get(alerta=alerta,miembro=miembro)

        return cuestionario




"""Serializer para mostrar la informacion de una o unas señas particulares"""
class senaSerializer(serializers.ModelSerializer):

    sena_particular = SenasParticularesSerializer()
    ubicacion_corporal = UbicacionCorporalSerializer()

    class Meta:
        model = UsuariaHasSenaUbicacion
        fields = (
            'descripcion',
            'sena_particular',
            'ubicacion_corporal',
        )

"""Serializer para registrar senas particulares de una usuaria"""
class senaCrearSerializer(serializers.Serializer):

    username = serializers.CharField()
    descripcion = serializers.CharField(max_length=200)
    nombre_ubicacion_corporal = serializers.CharField()
    nombre_sena_particular = serializers.CharField()

    def validate(self,data):

        #validar si el nombre de la ubicacion corporal existe
        try:
            ubicacion = UbicacionCorporal.objects.get(
                nombre_ubicacion_corporal=data['nombre_ubicacion_corporal']
            )
        except UbicacionCorporal.DoesNotExist:
            raise serializers.ValidationError('Esta ubicacion corporal no existe.')

        #validar que la seña particular existe
        try:
            sena = SenasParticulares.objects.get(nombre_sena_particular=data['nombre_sena_particular'])
        except SenasParticulares.DoesNotExist:
            raise serializers.ValidationError('Este tipo de sena particualr no existe.')

        #validar que la usuaria exista
        try:
            usuaria = Usuaria.objects.get(persona__username=data['username'])
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Esta usuaria no existe.')

        #validar que no se vuelva a registrar esta seña particular
        try:
            sena = UsuariaHasSenaUbicacion.objects.get(
                usuaria=usuaria,
                ubicacion_corporal=ubicacion,
                sena_particular=sena
            )
            raise serializers.ValidationError('Ya registraste esta sena particular.')
        except UsuariaHasSenaUbicacion.DoesNotExist:
            pass

        return data

    def create(self,data):

        #instancia de la usuaria
        usuaria = Usuaria.objects.get(persona__username=data['username'])

        #instancia de la ubicacion corporal
        ubicacion = UbicacionCorporal.objects.get(
            nombre_ubicacion_corporal=data['nombre_ubicacion_corporal']
        )

        #instancia de la sena particular
        senaParticular = SenasParticulares.objects.get(
            nombre_sena_particular=data['nombre_sena_particular']
        )

        #registrar la sena corporal de la usuaria
        sena = UsuariaHasSenaUbicacion.objects.create(
            usuaria=usuaria,
            descripcion=data['descripcion'],
            ubicacion_corporal=ubicacion,
            sena_particular=senaParticular
        )

        return sena

"""Serializer para actualizar la descripcion de una seña particular"""
class senaActualizarSerializer(serializers.Serializer):

    username = serializers.CharField()
    descripcion = serializers.CharField(max_length=200)
    nombre_ubicacion_corporal = serializers.CharField()
    nombre_sena_particular = serializers.CharField()

    def validate(self,data):

        #isntancia de la ubicacion corporal
        try:
            ubicacion = UbicacionCorporal.objects.get(
                nombre_ubicacion_corporal=data['nombre_ubicacion_corporal']
            )
        except UbicacionCorporal.DoesNotExist:
            raise serializers.ValidationError('Esta ubicacion corporal no existe.')

        #instancia de la seña particular
        try:
            sena = SenasParticulares.objects.get(nombre_sena_particular=data['nombre_sena_particular'])
        except SenasParticulares.DoesNotExist:
            raise serializers.ValidationError('Esta tipo de sena no existe.')

        #instancia de la usuaria
        try:
            usuaria = Usuaria.objects.get(persona__username=data['username'])
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Informacion de la usuaria incorrecta.')

        #instancia de la seña particular
        try:
            sena = UsuariaHasSenaUbicacion.objects.get(
                usuaria=usuaria,
                ubicacion_corporal=ubicacion,
                sena_particular=sena
            )            
        except UsuariaHasSenaUbicacion.DoesNotExist:
            raise serializers.ValidationError('No se tiene registrada esta sena particular.')

        #verificar que la descripcion no sea igual
        if sena.descripcion == data['descripcion']:
            raise serializers.ValidationError('La descripcion no puede ser igual.')

        return data

    def create(self,data):
        #salvar la nueva descripcion

        #instancia de la usuaria 
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #instancia de la sena particular
        sena = SenasParticulares.objects.get(nombre_sena_particular=data['nombre_sena_particular'])
        
        #instancia de la ubicacion corporal
        ubicacion = UbicacionCorporal.objects.get(nombre_ubicacion_corporal=data['nombre_ubicacion_corporal'])

        #instancia de la seña particular
        sena = UsuariaHasSenaUbicacion.objects.get(
            usuaria=usuaria,
            sena_particular=sena,
            ubicacion_corporal=ubicacion
        )

        #guardar la nueva descripcion
        sena.descripcion = data['descripcion']
        sena.save()

        return sena

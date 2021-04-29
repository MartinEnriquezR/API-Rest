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

"""Serializer para el signup de una persona"""
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
            raise serializers.ValidationError('El password nuevo debe de ser igual')

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



"""Serializer para que una usuaria que se regustra dentro del sistema"""
class usuariaSignupSerializer(serializers.Serializer):

    #campos de la persona
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
        """validacion los datos de la persona"""

        passwd = data['password']
        passwdConf = data['password_confirmation']
        genero = data['genero']
        fecha_nacimiento = data['fecha_nacimiento']
        today = date.today()
        diferenciaDias = today - fecha_nacimiento

        #validar las contraseñas, deben ser iguales
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

        try:
            EstadoCivil.objects.get(estado_civil=data['estado_civil'])
        except EstadoCivil.DoesNotExist:
            raise serializers.ValidationError('Este tipo de estado_civil no se encuentra registrado')

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

        #registro de la o las enfermedades que padece la usuaria
        enfermedades = data.pop('enfermedades')
        for enfermedadData in enfermedades:
            usuaria.enfermedades.add(
                #objeto de la enfermedad
                Enfermedad.objects.get(nombre_enfermedad=enfermedadData['nombre_enfermedad'])
            )
        usuaria.save()

        #obtener el token
        self.context['persona'] = persona
        token, created = Token.objects.get_or_create(user=self.context['persona'])
        return persona, token.key

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

    def validate(self,data):
        #validar que exista cada una de las opciones
        
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
            TexturaCabello.objects.get(estado_civil=data['estado_civil'])
        except TexturaCabello.DoesNotExist:
            raise serializers.ValidationError('Esta textura de cabello no es valida')

        return data

    def create(self,data):
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #instancias 
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
                raise serializers.ValidationError('Numero de serie incorrecto')
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
            raise serializers.ValidationError('Username invalido')

        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Username invalido')

        #encontrar si la usuaria tiene este dispositivo asociado
        try:
            dispositivo = DispositivoRastreador.objects.get(
                numero_serie = data['numero_serie'],
                usuaria= usuaria
            )
        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Este dispositivo no existe')

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
            raise serializers.ValidationError('Username incorrecto')
        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Username incorrecto')

        #encontrar el dispositivo
        try:
            DispositivoRastreador.objects.get(
                numero_serie=data['numero_serie'],
                usuaria = usuaria
            )
        except DispositivoRastreador.DoesNotExist:
            raise serializers.ValidationError('Numero de serie incorrecto')

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




"""Nombre y clave de acceso de un grupo de confianza"""
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
            grupo = Grupo.objects.get(usuaria=usuaria)
            raise serializers.ValidationError('La usuaria ya tiene un grupo de confianza')
        except Grupo.DoesNotExist:
            pass

        #validar la clave de acceso, que no este en uso por otro grupo
        seed(1)
        while True:
            clave = randint(0,999999)
            try:
                Grupo.objects.get(clave_acceso=str(clave))
            except Grupo.DoesNotExist:
                self.context['clave'] = str(clave)
                break

        return(data)

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

"""Informacion de los miembros"""
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
            raise serializers.ValidationError('No existe ningun grupo con esta clave de acceso')

        #validar que el limite de usuarios dentro del grupo
        totalMiembros = grupo.integrantes.all().count()
        if totalMiembros == 5:
            raise serializers.ValidationError('No se pueden agregar mas miembros a este grupo')

        #validar que no se vuelva a unir a un grupo esta persona
        persona = Persona.objects.get(username=data['username'])

        try:
            Miembros.objects.get(grupo=grupo, persona=persona)
            raise serializers.ValidationError('Ya formas parte de este grupo de confianza')
        except Miembros.DoesNotExist:
            pass

        return(data)

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
            admin = Persona.objects.get(username =data['username_usuaria'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username invalido')
        try:
            usuaria = Usuaria.objects.get(persona=admin)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Username invalido')
        try:
            grupo = Grupo.objects.get(usuaria=usuaria)
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('La usuaria no tiene un grupo de confianza')

        #saber si el contacto de confianza existe
        try:
            contacto = Persona.objects.get(username =data['username_persona'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username del contacto de confianza incorrecto')

        #saber si en este grupo tiene a el miembro
        try:
            Miembros.objects.get(grupo=grupo ,persona= contacto)
        except Miembros.DoesNotExist:
            raise serializers.ValidationError('Este contacto de confianza no es miembro de este grupo')

        return data

    def create(self,data):
        #instancia de la usuaria
        persona = Persona.objects.get(username =data['username_usuaria'])
        usuaria = Usuaria.objects.get(persona=persona)

        #grupo de la usuaria
        grupo = Grupo.objects.get(usuaria=usuaria)

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
        #verificar que la usuaria exista segun el username proporcionado
        try:
            persona = Persona.objects.get(username =data['username'])
        except Persona.DoesNotExist:
            raise serializers.ValidationError('Username invalido')
        try:
            usuaria = Usuaria.objects.get(persona = persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Username invalido')

        #verificar que el grupo exista
        try:
            grupo = Grupo.objects.get(usuaria=usuaria)
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('Esta usuaria no tiene ningun grupo')

        #verificar que el nombre nuevo del grupo sea diferente
        if grupo.nombre == data['nombre']:
            raise serializers.ValidationError('El nuevo nombre debe de ser diferente')

        return data

    def create(self,data):
        #instancia de la usuaria
        persona = Persona.objects.get(username =data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #grupo de la usuaria
        grupo = Grupo.objects.get(usuaria = usuaria)

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

        return ubicacion

"""Serializer para que el dispositivo sepa si la alerta fue desactivada"""
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

        #instancia de la usuaria
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #validar que el grupo de la usuaria tenga la alerta activa
        try:
            grupo = Grupo.objects.get(usuaria=usuaria,estado_alerta=True)
        except Grupo.DoesNotExist:
            raise serializers.ValidationError('Este grupo no tiene ninguna alerta activa')

        #encontrar un dispositivo o dispositivos de la usuaria que coincida con el pin desactivador
        d = DispositivoRastreador.objects.filter(usuaria=usuaria,pin_desactivador=data['pin_desactivador'])
        if not d:
            raise serializers.ValidationError('Pin incorrecto')

        #validar que la alerta exista
        try:
            Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Esta alerta no existe')


        return data




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

        #saber si el grupo existe
        #saber si el grupo tiene una alerta activa
        try:
            admin = Persona.objects.get(username=data['username_usuaria'])
            usuaria = Usuaria.objects.get(persona=admin)
            grupo = Grupo.objects.get(usuaria=usuaria,estado_alerta=True)
        except:
            raise serializers.ValidationError('Informacion del grupo incorrecta')

        #saber si existe una alerta con este nombre
        #saber si la alerta forma parte de este grupo
        try:
            alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Informacion de la alerta incorrecta')

        #saber si la persona es miembro de este grupo
        try:
            persona = Persona.objects.get(username=data['username_persona'])
            miembro = Miembros.objects.get(grupo=grupo,persona=persona)
        except:
            raise serializers.ValidationError('Esta persona no es miembro del grupo')

        #saber si no ha contestado este cuestionario previamente
        try:
            Cuestionario.objects.get(alerta=alerta,miembro=miembro)
            raise serializers.ValidationError('Ya respondiste este cuestionario')
        except Cuestionario.DoesNotExist:
            pass

        return data

    def create(self,data):

        #instancia del tipo de circunstancia
        circunstancia = Circunstancia.objects.get(tipo_circunstancia=data['tipo_circunstancia'])

        #instancia del lazo
        lazo = Lazo.objects.get(lazo=data['lazo'])

        #instancia del grupo
        admin = Persona.objects.get(username=data['username_usuaria'])
        usuaria = Usuaria.objects.get(persona=admin)
        grupo = Grupo.objects.get(usuaria=usuaria)

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

        #saber si el grupo existe
        #saber si el grupo tiene una alerta activa
        try:
            admin = Persona.objects.get(username=data['username_usuaria'])
            usuaria = Usuaria.objects.get(persona=admin)
            grupo = Grupo.objects.get(usuaria=usuaria,estado_alerta=True)
        except:
            raise serializers.ValidationError('Informacion del grupo incorrecta')

        #saber si existe una alerta con este nombre
        #saber si la alerta forma parte de este grupo
        try:
            alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Informacion de la alerta incorrecta')

        #saber si la persona es miembro de este grupo
        try:
            persona = Persona.objects.get(username=data['username_persona'])
            miembro = Miembros.objects.get(grupo=grupo,persona=persona)
        except:
            raise serializers.ValidationError('Esta persona no es miembro del grupo')

        #saber si ya ha contestado el cuestionario
        try:
            Cuestionario.objects.get(alerta=alerta,miembro=miembro)
        except Cuestionario.DoesNotExist:
            raise serializers.ValidationError('Aun no haz contestado el cuestionario')

        return data

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
            admin = Persona.objects.get(username=data['username_usuaria'])
            usuaria = Usuaria.objects.get(persona=admin)
            grupo = Grupo.objects.get(usuaria=usuaria)
        except:
            raise serializers.ValidationError('Informacion del grupo invalida')

        #encontrar la alerta
        try:
            alerta = Alerta.objects.get(grupo=grupo,nombre_alerta=data['nombre_alerta'])
        except Alerta.DoesNotExist:
            raise serializers.ValidationError('Informacion de la alerta invalida')

        #encontrar el miembro
        try:
            persona = Persona.objects.get(username=data['username_persona'])
            miembro = Miembros.objects.get(grupo=grupo,persona=persona)
        except:
            raise serializers.ValidationError('No eres parte de este grupo')

        #encontrar el cuestionario
        try:
            cuestionario = Cuestionario.objects.get(miembro=miembro,alerta=alerta)
        except Cuestionario.DoesNotExist:
            raise serializers.ValidationError('Aun no haz respondido el cuestionario')

        return data

    def create(self,data):

        #grupo
        admin = Persona.objects.get(username=data['username_usuaria'])
        usuaria = Usuaria.objects.get(persona=admin)
        grupo = Grupo.objects.get(usuaria=usuaria)

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
            ubicacion = UbicacionCorporal.objects.get(nombre_ubicacion_corporal=data['nombre_ubicacion_corporal'])
        except UbicacionCorporal.DoesNotExist:
            raise serializers.ValidationError('Esta ubicacion corporal no existe.')

        #validar que la seña particular existe
        try:
            sena = SenasParticulares.objects.get(nombre_sena_particular=data['nombre_sena_particular'])
        except SenasParticulares.DoesNotExist:
            raise serializers.ValidationError('Este tipo de sena particualr no existe.')

        #validar que la usuaria exista
        admin = Persona.objects.get(username=data['username'])
        try:
            usuaria = Usuaria.objects.get(persona=admin)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Esta usuaria no existe.')

        #validar que no se vuelva a registrar esta seña particular
        try:
            sena = UsuariaHasSenaUbicacion.objects.get(
                usuaria=usuaria,
                ubicacion_corporal=ubicacion,
                sena_particular=sena
            )
            raise serializers.ValidationError('Ya registraste esta sena particular')
        except UsuariaHasSenaUbicacion.DoesNotExist:
            pass

        return data


    def create(self,data):

        #instancia de la usuaria
        persona = Persona.objects.get(username=data['username'])
        usuaria = Usuaria.objects.get(persona=persona)

        #instancia de la ubicacion corporal
        ubicacion = UbicacionCorporal.objects.get(nombre_ubicacion_corporal=data['nombre_ubicacion_corporal'])

        #instancia de la sena particular
        senaParticular = SenasParticulares.objects.get(nombre_sena_particular=data['nombre_sena_particular'])

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
            ubicacion = UbicacionCorporal.objects.get(nombre_ubicacion_corporal=data['nombre_ubicacion_corporal'])
        except UbicacionCorporal.DoesNotExist:
            raise serializers.ValidationError('Esta ubicacion corporal no existe')

        #instancia de la seña particular
        try:
            sena = SenasParticulares.objects.get(nombre_sena_particular=data['nombre_sena_particular'])
        except SenasParticulares.DoesNotExist:
            raise serializers.ValidationError('Esta tipo de sena no existe')

        #instancia de la usuaria
        persona = Persona.objects.get(username=data['username'])
        try:
            usuaria = Usuaria.objects.get(persona=persona)
        except Usuaria.DoesNotExist:
            raise serializers.ValidationError('Informacion de la usuaria incorrecta')

        #instancia de la seña particular
        try:
            sena = UsuariaHasSenaUbicacion.objects.get(
                usuaria=usuaria,
                ubicacion_corporal=ubicacion,
                sena_particular=sena
            )            
        except UsuariaHasSenaUbicacion.DoesNotExist:
            raise serializers.ValidationError('No se tiene registrada esta sena particular')

        #verificar que la descripcion no sea igual
        if sena.descripcion == data['descripcion']:
            raise serializers.ValidationError('La descripcion no puede ser igual')

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

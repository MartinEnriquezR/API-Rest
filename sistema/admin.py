from django.contrib import admin
from .models import *

#definir los modelos del sistema
admin.site.register(Persona)
admin.site.register(Usuaria)
admin.site.register(DispositivoRastreador)
admin.site.register(GrupoConfianza)
admin.site.register(Alerta)
admin.site.register(Cuestionario)
admin.site.register(Ubicacion)
admin.site.register(UsuariaHasSenaUbicacion)

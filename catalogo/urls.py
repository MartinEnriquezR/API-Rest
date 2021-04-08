#librerias de django
from django.urls import path

#vistas del catalogo
from .views import *

urlpatterns=[
    path('formas-rostro/',listarFormaRostro),
    path('colores-cabello/',listarColorCabello),
    path('colores-piel/',listarColorPiel),
    path('tipos-cejas/',listarTipoCejas),
    path('paises/',listarPais),
    path('tipos-nariz/',listarTipoNariz),
    path('complexiones/',listarComplexion),
    path('colores-ojos/',listarColorOjos),
    path('texturas-cabello/',listarTexturaCabello),
    path('enfermedades/',listarEnfermedades),
    path('ubicaciones-corporales/',listarUbicacionCorporal),
    path('circunstancias/',listarCircunstancia),
    path('lazos/',listarLazo),
    path('senas-particualres/',listarSenasParticulares),
    
]

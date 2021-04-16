#librerias de django
from django.urls import path, include

#librerias de django rest framewoek
from rest_framework.routers import DefaultRouter

#importar las vistas 
from .views import *

router = DefaultRouter()

router.register(r'formas-rostro', formaRostroViewSet, basename = 'formas-rostro')
router.register(r'colores-cabello', colorCabelloViewSet, basename = 'colores-cabello')
router.register(r'colores-piel', colorPielViewSet, basename = 'colores-piel')
router.register(r'tipos-cejas', tipoCejasViewSet, basename = 'tipos-cejas')
router.register(r'paises', paisViewSet, basename = 'paises')
router.register(r'tipos-nariz', tipoNarizViewSet, basename = 'tipos-nariz')
router.register(r'complexiones', complexionViewSet, basename = 'complexiones')
router.register(r'colores-ojos', colorOjosViewSet, basename = 'colores-ojos')
router.register(r'textura-cabello', texturaCabelloViewSet, basename = 'textura-cabello')
router.register(r'enfermedades', enfermedadViewSet, basename = 'enfermedades')
router.register(r'ubicaciones-corporales', ubicacionCorporalViewSet, basename = 'ubicaciones-corporales')
router.register(r'circunstancias', circunstanciaViewSet, basename = 'circunstancias')
router.register(r'lazos', lazoViewSet, basename = 'lazos')
router.register(r'senas-particulares', senasParticularesViewSet, basename = 'senas-particulares')
router.register(r'estados-civiles',estadoCivilViewSet, basename = 'estados-civiles')

urlpatterns = [
    path('',include(router.urls))
]


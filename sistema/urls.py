#librerias de django
from django.urls import path, include

#django rest framework
from rest_framework.routers import DefaultRouter

#vista de login del sistema
from .views import *

router = DefaultRouter()


router.register(r'persona',personaViewSet,basename='persona')
router.register(r'usuaria',usuariaViewSet,basename='usuaria')
router.register(r'dispositivo',dispositivoViewSet,basename='dispositivo')
router.register(r'grupo',grupoViewSet,basename='grupo')
router.register(r'alerta',alertaViewSet,basename='alerta')
router.register(r'cuestionario',cuestionarioViewSet,basename='cuestionario')
router.register(r'senas',senasViewSet,basename='senas')



urlpatterns = [
    path('',include(router.urls))
]

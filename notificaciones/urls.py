#librerias de django
from django.urls import path, include

#django rest framework
from rest_framework.routers import DefaultRouter

#vista de login del sistema
from .views import *

#firebase cloud messaging
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


router = DefaultRouter()

#registro de la url para guardar el endpoint del dispositivo del usuario
router.register(
    r'registrar-notificacion-token',
    FCMDeviceAuthorizedViewSet,
    basename='registrar-notificacion-token'
)


urlpatterns = [
    path('',include(router.urls))
]

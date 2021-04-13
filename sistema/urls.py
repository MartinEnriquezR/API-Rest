#librerias de django
from django.urls import path, include

#django rest framework
from rest_framework.routers import DefaultRouter

#vista de login del sistema
from .views import *

router = DefaultRouter()


router.register(r'persona',personaViewSet,basename='persona')
router.register(r'usuaria',usuariaViewSet,basename='usuaria')
router.register(r'grupo',grupoViewSet,basename='grupo')



urlpatterns = [
    path('',include(router.urls))
]

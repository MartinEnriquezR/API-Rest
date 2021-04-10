#librerias de django
from django.urls import path, include

#django rest framework
from rest_framework.routers import DefaultRouter

#vista de login del sistema
from .views import *

router = DefaultRouter()

#login
router.register(r'login',personaLoginViewSet,basename = 'login')

#signup
router.register(r'persona/signup',personaSignupViewSet,basename = 'persona-signup')
router.register(r'usuaria/signup',usuariaSignupViewSet,basename = 'usuaria-signup')

router.register(r'prueba',prueba, basename='prueba')


urlpatterns = [
    path('',include(router.urls))
]

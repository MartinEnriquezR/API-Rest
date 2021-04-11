#librerias de django
from django.urls import path, include

#django rest framework
from rest_framework.routers import DefaultRouter

#vista de login del sistema
from .views import *

router = DefaultRouter()

#login
#url=login/
router.register(r'login',personaLoginViewSet,basename = 'login')

#signup
#url=persona/signup/
#url=usuaria/signup/
router.register(r'persona/signup',personaSignupViewSet,basename = 'persona-signup')
router.register(r'usuaria/signup',usuariaSignupViewSet,basename = 'usuaria-signup')

#listar informacion, borrar persona y modificar datos de persona
#url = persona/<username>/
router.register(r'persona',personaViewSet,basename='persona')





urlpatterns = [
    path('',include(router.urls))
]

#librerias de django
from django.urls import path

#vista de login del sistema
from .views import *

urlpatterns=[
    #login
    path('usuarios/login/',userLoginAPIView.as_view(),name='login'),
    #signup 
    path('persona/signup/',personaSignupAPIView.as_view(),name='persona_signup'),
    path('usuaria/signup/',usuariaSignupAPIView.as_view(),name='usuaria_signup'),
    #asociar el dispositivo rastreador
    path('usuaria/asociar-dispositivo/',dispositivoAsociarAPIView.as_view(),name='asociar-dispositivo'),
    #creacion de un grupo
    path('usuaria/create-group/',grupoCrearAPIView.as_view(),name='group-create'),
    #obtener datos del grupo de confianza
    path('usuaria/group-info/',grupoInfoAPIView.as_view(),name='group-info'),
]

"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    #sitio de administracion de django
    path('admin/', admin.site.urls),
    
    #ulrs del catalogo
    path('',include(('catalogo.urls','catalogo'),namespace='catalogo')),
    
    #ulrs del sistema
    path('',include(('sistema.urls','sistema'),namespace='sistema')),

    #urls de las graficas
    path('',include(('graficas.urls','graficas'),namespace='graficas')),

    #urls de las notificaciones
    path('',include(('notificaciones.urls','notificaciones'),namespace='notificaciones')),
    
]

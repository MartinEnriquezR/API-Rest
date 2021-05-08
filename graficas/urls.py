#librerias de django
from django.urls import path, include

#django rest framework
from rest_framework.routers import DefaultRouter

#vistas de las graficas
from .views import *

router = DefaultRouter()

router.register(r'graficas',graficasViewSet,basename='graficas')

urlpatterns = [
    path('',include(router.urls))
]
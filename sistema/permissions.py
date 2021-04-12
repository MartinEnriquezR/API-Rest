"""Definir los permisos del usuario"""

#django rest framework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Permitir el acceso solo a los dueños de la cuenta"""
    def has_object_permission(self,request,view,obj):
        #checha que el obj y el user sean los mismos"""
        return request.user == obj
        
from rest_framework import permissions
from api.models import *


# SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class isOwnerReadOnlyOrisAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if isinstance(obj, PaymentTicket):
                return (obj.owner == request.user) or request.user.is_staff
            elif isinstance(obj, Client):
                return (obj.pk == request.user) or request.user.is_staff

        return obj.owner == request.user

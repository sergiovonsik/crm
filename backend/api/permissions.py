from rest_framework import permissions
from api.models import *


# SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class AdminGetAnyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_staff
        if request.method == 'POST':
            return True


class IsOwnerReadOnlyOrisAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if isinstance(obj, PaymentTicket):
                return (obj.owner == request.user) or request.user.is_staff
            elif isinstance(obj, Client):
                return obj == request.user or request.user.is_staff

        return request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PATCH']:
            return obj == request.user or request.user.is_staff
        else:
            return request.user.is_staff

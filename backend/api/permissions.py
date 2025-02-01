from rest_framework import permissions

# SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class isOwnerReadOnlyOrisAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return (obj.owner == request.user) or request.user.is_staff

        return obj.owner == request.user

from rest_framework import permissions

class IsRider(permissions.BasePermission):
    """
    Custom permission to allow only riders to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_rider
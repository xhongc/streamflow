from rest_framework.permissions import BasePermission


class ApiPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user and request.user.is_authenticated

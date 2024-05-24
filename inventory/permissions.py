from rest_framework.permissions import BasePermission


class IsNotManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name='managers').exists():
            return False

        return True

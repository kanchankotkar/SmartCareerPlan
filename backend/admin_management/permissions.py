from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        if not user:
            return False

        if user.__class__.__name__ == "AnonymousUser":
            return False

        return getattr(user, "is_admin", False)
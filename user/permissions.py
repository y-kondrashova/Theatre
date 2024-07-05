from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

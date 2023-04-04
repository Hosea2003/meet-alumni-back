from rest_framework.permissions import BasePermission, IsAuthenticated


class IsCollegeAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user:
            return False
        return user.isAdminCollege

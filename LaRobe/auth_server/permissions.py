from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['junior_admin', 'senior_admin']

class SeniorAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'senior_admin'

class NotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != "blocked"
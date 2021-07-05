from rest_framework import permissions


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin


class CanAccessCustomUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, user_object):
        return super().has_permission(request, view) and (request.user == user_object)

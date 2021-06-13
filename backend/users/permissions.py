from rest_framework import permissions


class CanAccessCustomUser(permissions.BasePermission):
    def has_object_permission(self, request, view, user_object):
        return request.user.is_authenticated and (request.user.is_admin or request.user == user_object)


class CanChangeCustomUserPassword(permissions.BasePermission):
    def has_object_permission(self, request, view, user_object):
        return request.user.is_authenticated and request.user == user_object


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

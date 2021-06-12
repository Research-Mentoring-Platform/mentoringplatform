from rest_framework import permissions


class CanAccessMentee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_admin or request.user == obj.user)

from rest_framework import permissions


class IsMentor(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_mentor


class CanAccessMentor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and (request.user == obj.user)


class CanAccessMentorEducation(CanAccessMentor):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.mentor)


class CanAccessMentorResearch(CanAccessMentor):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.mentor)


class CanRetrieveMentor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return True if request.user == obj.user else obj.is_verified

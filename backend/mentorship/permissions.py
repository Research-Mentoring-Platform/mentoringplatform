from rest_framework import permissions as rest_permissions


class CanAccessMentorshipApp(rest_permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_mentor:
            return super().has_permission(request,
                                          view) and request.user.mentor.profile_completed and request.user.mentor.is_verified
        elif request.user.is_mentee:
            return super().has_permission(request, view) and request.user.mentee.profile_completed

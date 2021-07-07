from rest_framework import permissions as rest_permissions


class CanAccessMentorshipApp(rest_permissions.IsAuthenticated):
    def has_permission(self, request, view):
        base_permission = super().has_permission(request, view)
        if request.user.is_mentor:
            return base_permission and request.user.mentor.profile_completed and request.user.mentor.is_verified
        elif request.user.is_mentee:
            return base_permission and request.user.mentee.profile_completed
        return False  # Admin


class CanAccessMentorship(CanAccessMentorshipApp):
    def has_object_permission(self, request, view, obj):
        base_permission = super().has_permission(request, view)
        if request.user.is_mentor:
            return base_permission and (obj.mentor == request.user.mentor)
        elif request.user.is_mentee:
            return base_permission and (obj.mentee == request.user.mentee)


class CanAccessMentorshipRequest(CanAccessMentorshipApp):
    def has_object_permission(self, request, view, obj):
        base_permission = super().has_permission(request, view)
        if request.user.is_mentor:
            return base_permission and (obj.mentor == request.user.mentor)
        elif request.user.is_mentee:
            return base_permission and (obj.mentee == request.user.mentee)
        return False  # Admin


class CanAccessMeeting(CanAccessMentorshipApp):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and (request.user == obj.mentorship.mentor.user or
                                                          request.user == obj.mentorship.mentee.user)


class CanAccessMeetingSummary(CanAccessMentorshipApp):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and (request.user == obj.meeting.mentorship.mentor.user or
                                                          request.user == obj.meeting.mentorship.mentee.user)


class CanAccessMilestone(CanAccessMentorshipApp):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and (request.user == obj.mentorship.mentor.user or
                                                          request.user == obj.mentorship.mentee.user)

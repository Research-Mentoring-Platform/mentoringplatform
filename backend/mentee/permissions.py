from rest_framework import permissions

from mentorship.models import Mentorship, MentorshipStatus, MentorshipRequest, MentorshipRequestStatus


class IsMentee(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_mentee


class CanAccessMentee(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and (request.user == obj.user)


class CanAccessMenteeEducation(CanAccessMentee):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.mentee)


class CanAccessMenteeResearch(CanAccessMentee):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.mentee)


class CanRetrieveMentee(permissions.IsAuthenticated):
    """
    This permission class is allowing two cases:
    1. If the request is made by a mentor, they can access a mentee only if an ongoing mentorship exists with the
        specified mentee or a pending mentorship-request exists from the specified mentee to the mentor
    2. If the request is made by the mentee accessing their own mentee-profile.
    TODO confirm this from sir.
    """

    def has_object_permission(self, request, view, obj):
        base_condition = super().has_permission(request, view)
        if request.user.is_mentor:
            allow1 = Mentorship.objects.filter(mentor=request.user.mentor, mentee=obj,
                                               status=MentorshipStatus.ONGOING).exists()
            allow2 = MentorshipRequest.objects.filter(mentor=request.user.mentor, mentee=obj,
                                                      status=MentorshipRequestStatus.REQUEST_PENDING).exists()
            return base_condition and (allow1 or allow2)

        elif request.user.is_mentee:
            return base_condition and (request.user == obj.user)

        return False


class CanRetrieveMenteeEducation(CanRetrieveMentee):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.mentee)


class CanRetrieveMenteeResearch(CanRetrieveMentee):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.mentee)

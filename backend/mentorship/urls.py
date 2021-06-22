from django.urls import path, include
from rest_framework import routers

from mentorship.views import MentorshipRequestViewSet, MentorshipViewSet, MeetingViewSet, MeetingSummaryViewSet

router = routers.DefaultRouter()
router.register('mentorship', MentorshipViewSet)
router.register('request', MentorshipRequestViewSet)
router.register('meeting', MeetingViewSet)
router.register('meeting-summary', MeetingSummaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

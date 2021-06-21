from django.urls import path, include
from rest_framework import routers

from mentorship.views import MentorshipRequestViewSet, MentorshipViewSet, MeetingViewSet

router = routers.DefaultRouter()
router.register('mentorship', MentorshipViewSet)
router.register('request', MentorshipRequestViewSet)
router.register('meeting', MeetingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

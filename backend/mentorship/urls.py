from django.urls import path, include
from rest_framework import routers

from mentorship.views import MentorshipRequestViewSet, MentorshipViewSet

router = routers.DefaultRouter()
router.register('mentorship', MentorshipViewSet)
router.register('request', MentorshipRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

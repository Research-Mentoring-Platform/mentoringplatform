from django.urls import path, include
from rest_framework import routers

from mentorship.views import MentorshipRequestViewSet

router = routers.DefaultRouter()
router.register('request', MentorshipRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers

from mentorship.views import EducationViewSet, ResearchViewSet

router = routers.DefaultRouter()
router.register('education', EducationViewSet)
router.register('research', ResearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers

from mentorship.views import EducationViewSet

router = routers.DefaultRouter()
router.register('education', EducationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

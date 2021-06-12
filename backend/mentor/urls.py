from django.urls import path, include
from rest_framework import routers
from .views import MentorViewSet

router = routers.DefaultRouter()
router.register('mentor', MentorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

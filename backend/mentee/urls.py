from django.urls import path, include
from rest_framework import routers
from .views import MenteeViewSet

router = routers.DefaultRouter()
router.register('mentee', MenteeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

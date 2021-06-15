from django.urls import path, include
from rest_framework import routers

from .views import MentorViewSet, MentorResponsibilityViewSet, MentorDepartmentViewSet, MentorDesignationViewSet, \
    MentorDisciplineViewSet, MentorEducationViewSet, MentorResearchViewSet

router = routers.DefaultRouter()
router.register('mentor', MentorViewSet)
router.register('responsibility', MentorResponsibilityViewSet)
router.register('department', MentorDepartmentViewSet)
router.register('designation', MentorDesignationViewSet)
router.register('discipline', MentorDisciplineViewSet)
router.register('education', MentorEducationViewSet)
router.register('research', MentorResearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers

from .views import MenteeViewSet, MenteeDepartmentViewSet, MenteeDesignationViewSet, MenteeDisciplineViewSet, \
    MenteeEducationViewSet, MenteeResearchViewSet

router = routers.DefaultRouter()
router.register('mentee', MenteeViewSet)
router.register('department', MenteeDepartmentViewSet)
router.register('designation', MenteeDesignationViewSet)
router.register('discipline', MenteeDisciplineViewSet)
router.register('education', MenteeEducationViewSet)
router.register('research', MenteeResearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

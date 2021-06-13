from django.urls import path, include
from rest_framework import routers
from .views import MenteeViewSet, MenteeDepartmentViewSet, MenteeDesignationViewSet, MenteeDisciplineViewSet

router = routers.DefaultRouter()
router.register('mentee', MenteeViewSet)
router.register('department', MenteeDepartmentViewSet)
router.register('designation', MenteeDesignationViewSet)
router.register('discipline', MenteeDisciplineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

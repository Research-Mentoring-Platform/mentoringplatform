from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomUserViewSet, CustomTokenObtainPairView

router = routers.DefaultRouter()
router.register('user', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
]

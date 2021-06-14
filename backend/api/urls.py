from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include('users.urls')),
    path('mentor/', include('mentor.urls')),
    path('mentee/', include('mentee.urls')),
    path('mentorship/', include('mentorship.urls'))
]

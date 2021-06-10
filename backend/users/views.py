from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from users.serializers import CustomUserSerializer


class CreateCustomUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserSerializer
    queryset = get_user_model().objects.all()

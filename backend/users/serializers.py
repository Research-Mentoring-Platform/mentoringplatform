# from django.contrib.auth.password_validation import validate_password
# from users.models import CustomUser
# from rest_framework import serializers
#
#
# class CustomUserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(validators=[validate_password])
#
#     class Meta:
#         model = CustomUser
#         fields = ('phone_number', 'password', 'first_name', 'gender', 'last_name', 'location', 'type')
#
#     #  https://stackoverflow.com/a/27586289/5394180
#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
#
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             if attr == 'password':
#                 instance.set_password(value)
#             else:
#                 setattr(instance, attr, value)
#         instance.save()
#         return instance

from rest_framework import serializers

from mentee.models import Mentee, MenteeDesignation, MenteeDepartment, MenteeDiscipline


class MenteeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='uid',
                                        queryset=Mentee.objects.all(),
                                        read_only=True)
    designation = serializers.SlugRelatedField(slug_field='uid',
                                               queryset=MenteeDesignation.objects.all(),
                                               read_only=False,
                                               required=True,
                                               allow_null=False)
    department = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MenteeDepartment.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)
    discipline = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MenteeDiscipline.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    class Meta:
        model = Mentee
        fields = '__all__'
        read_only_fields = ('uid', 'rating', 'profile_completed')

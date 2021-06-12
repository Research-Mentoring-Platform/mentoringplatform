from rest_framework import serializers
from mentee.models import MenteeDesignation
from mentor.models import Mentor, MentorDesignation, MentorDepartment, MentorDiscipline, MentorResponsibility


class MentorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='uid',
                                        read_only=True)

    designation = serializers.SlugRelatedField(slug_field='uid',
                                               queryset=MentorDesignation.objects.all(),
                                               read_only=False,
                                               required=True,
                                               allow_null=False)

    department = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MentorDepartment.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    discipline = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MentorDiscipline.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    accepted_mentee_types = serializers.SlugRelatedField(slug_field='uid',
                                                         queryset=MenteeDesignation.objects.all(),
                                                         read_only=False,
                                                         many=True,
                                                         required=False,
                                                         allow_null=True)
    responsibilities = serializers.SlugRelatedField(slug_field='uid',
                                                    queryset=MentorResponsibility.objects.all(),
                                                    read_only=False,
                                                    many=True,
                                                    required=False,
                                                    allow_null=True)

    class Meta:
        model = Mentor
        exclude = ('id',)
        read_only_fields = ('uid', 'rating', 'profile_completed', 'is_verified', 'user')


class MentorResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorResponsibility
        exclude = ('id',)
        read_only_fields = ('uid', 'description',)


class MentorDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorDepartment
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MentorDesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorDesignation
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MentorDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorDiscipline
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)

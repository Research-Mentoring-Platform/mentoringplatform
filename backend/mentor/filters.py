import django_filters

from mentor.models import Mentor, MentorEducation, MentorResearch


class MentorFilter(django_filters.FilterSet):
    designation = django_filters.UUIDFilter(field_name='designation__uid', lookup_expr='exact')
    department = django_filters.UUIDFilter(field_name='department__uid', lookup_expr='exact')
    discipline = django_filters.UUIDFilter(field_name='discipline__uid', lookup_expr='exact')

    class Meta:
        model = Mentor
        fields = ('designation__uid', 'department__uid', 'discipline__uid')


class MentorEducationFilter(django_filters.FilterSet):
    mentor = django_filters.UUIDFilter(field_name='mentor__uid', lookup_expr='exact', required=True)

    class Meta:
        model = MentorEducation
        fields = ('mentor__uid',)


class MentorResearchFilter(MentorEducationFilter):
    class Meta(MentorEducationFilter.Meta):
        model = MentorResearch

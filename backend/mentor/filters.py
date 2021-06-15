import django_filters

from mentor.models import Mentor


class MentorFilter(django_filters.FilterSet):
    designation = django_filters.UUIDFilter(field_name='designation__uid', lookup_expr='exact')
    department = django_filters.UUIDFilter(field_name='department__uid', lookup_expr='exact')
    discipline = django_filters.UUIDFilter(field_name='discipline__uid', lookup_expr='exact')

    class Meta:
        model = Mentor
        fields = ('designation__uid', 'department__uid', 'discipline__uid')

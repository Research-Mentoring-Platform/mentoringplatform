import django_filters

from mentee.models import MenteeEducation, MenteeResearch


class MenteeEducationFilter(django_filters.FilterSet):
    mentee = django_filters.UUIDFilter(field_name='mentee__uid', lookup_expr='exact', required=True)

    class Meta:
        model = MenteeEducation
        fields = ('mentee__uid',)


class MenteeResearchFilter(MenteeEducationFilter):
    class Meta(MenteeEducationFilter.Meta):
        model = MenteeResearch

import django_filters
from .models import UseCase, Capability, Stakeholder

class UseCaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    risk_level = django_filters.ChoiceFilter(choices=UseCase.RISK_LEVELS)
    status = django_filters.ChoiceFilter(choices=UseCase.STATUS_CHOICES)
    capabilities = django_filters.ModelMultipleChoiceFilter(
        queryset=Capability.objects.all(),
        widget=django_filters.widgets.CSVWidget
    )
    stakeholders = django_filters.ModelMultipleChoiceFilter(
        queryset=Stakeholder.objects.all(),
        widget=django_filters.widgets.CSVWidget
    )

    class Meta:
        model = UseCase
        fields = ['name', 'risk_level', 'status', 'capabilities', 'stakeholders']
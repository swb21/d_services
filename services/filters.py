from django_filters import rest_framework as filters

from services.models import WashingSchedule


class WashingScheduleFilter(filters.FilterSet):
    class Meta:
        model = WashingSchedule
        fields = [
            'washing_time',
        ]

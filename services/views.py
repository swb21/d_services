from django.db.models import Prefetch, Count
from rest_framework import authentication
from rest_framework.generics import CreateAPIView, ListAPIView

from services.models import User, WashingTime, WashingSchedule, WashingMachine
from services.serializers import UserSerializer, WashingTimeSerializer, WashingMachineSerializer, \
    WashingScheduleSerializer


class UserAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserSerializer
    queryset = User.objects.all()


class WashingTimeAPIView(ListAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = ()

    serializer_class = WashingTimeSerializer

    def get_queryset(self):
        """
        Gets time in which at least one machine is free
        by `date` and `dormitory` query parameters
        """
        queryset = WashingTime.objects.all()

        date = self.request.query_params.get('date', None)
        dormitory = self.request.query_params.get('dormitory', None)

        if date is not None and dormitory is not None:
            machines_count = WashingMachine.objects.filter(
                dormitory__number=dormitory, is_exploitable=True).count()
            busy_time = WashingSchedule.objects.values('time').annotate(
                cnt=Count('id')).filter(
                    cnt__exact=machines_count, date=date).values_list(
                        'time', flat=True)
            queryset = WashingTime.objects.exclude(id__in=busy_time)

        return queryset


class FreeWashingMachinesAPIView(ListAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = ()

    serializer_class = WashingMachineSerializer

    def get_queryset(self):
        """
        Gets free washing machines by `date`, `time` and
        `dormitory` query parameters
        """
        queryset = WashingMachine.objects.all()

        date = self.request.query_params.get('date', None)
        time = self.request.query_params.get('time', None)
        dormitory = self.request.query_params.get('dormitory', None)

        if date is not None and time is not None and dormitory is not None:
            busy_machines = WashingSchedule.objects.filter(
                user__profile__dormitory__number=dormitory,
                date=date,
                time=time).values_list(
                    'washing_machine', flat=True)
            queryset = WashingMachine.objects.filter(
                is_exploitable=True).exclude(id__in=busy_machines)

        return queryset


class WashingScheduleAPIView(CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = ()

    serializer_class = WashingScheduleSerializer
    queryset = WashingSchedule

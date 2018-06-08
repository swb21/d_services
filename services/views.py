from django.db.models import Count
from rest_framework import authentication, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from services.models import *
from services.serializers import *


class UserAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserSerializer
    queryset = User.objects.all()


class DormitoryAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        """
        Gets time in which at least one machine is free
        by `date` and `dormitory` query parameters
        """
        dormitories = [{
            'id': dormitory.id,
            'number': dormitory.number,
            'address': dormitory.address
        } for dormitory in Dormitory.objects.all()]

        return Response({'dormitories': dormitories})


class WashingTimeAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        """
        Gets time in which at least one machine is free
        by `date` and `dormitory` query parameters
        """
        date = self.request.query_params.get('date', None)
        dormitory = self.request.query_params.get('dormitory', None)

        if date is not None and dormitory is not None:
            machines_count = WashingMachine.objects.filter(
                dormitory__number=dormitory, is_exploitable=True).count()
            busy_time = WashingSchedule.objects.values('time').annotate(
                cnt=Count('id')).filter(
                    cnt__exact=machines_count, date=date).values_list(
                        'time', flat=True)
            free_time = [{
                'id': time.id,
                'time': time.time
            } for time in WashingTime.objects.exclude(id__in=busy_time)]

            return Response({'times': free_time})


class FreeWashingMachinesAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        """
        Gets time in which at least one machine is free
        by `date` and `dormitory` query parameters
        """
        date = request.query_params.get('date', None)
        time = request.query_params.get('time', None)
        dormitory = request.query_params.get('dormitory', None)

        if date is not None and time is not None and dormitory is not None:
            busy_machines = WashingSchedule.objects.filter(
                user__profile__dormitory__number=dormitory,
                date=date,
                time=time).values_list(
                    'washing_machine', flat=True)
            washing_machines = [{
                'id': washing_machine.id,
                'number': washing_machine.number
            } for washing_machine in WashingMachine.objects.filter(
                is_exploitable=True).exclude(id__in=busy_machines)]

            return Response({'washing_machines': washing_machines})

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


class WashingScheduleAPIView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = WashingScheduleSerializer
    queryset = WashingSchedule

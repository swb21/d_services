from django.db.models import Prefetch, Count
from rest_framework import authentication
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from services.models import User, WashingTime, WashingSchedule, WashingMachine
from services.serializers import UserSerializer, WashingTimeSerializer


class UserAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserSerializer
    queryset = User.objects.all()


class WashingTimeAPIView(ListAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    authentication_classes = ()
    permission_classes = ()

    serializer_class = WashingTimeSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.

        Получить записи из washing_time, количество которых в таблице washing_schedule меньше,
        чем количество рабочих машинок в общежитии пользователя
        """
        queryset = WashingTime.objects.all()

        date = self.request.query_params.get('date', None)
        dormitory = self.request.query_params.get('dormitory', None)

        if date is not None and dormitory is not None:
            machines_count = WashingMachine.objects.filter(dormitory=dormitory, is_exploitable=True).count()
            queryset = WashingSchedule.objects.values('time').annotate(cnt=Count('id')).filter(
                cnt__lt=machines_count)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     if self.request.query_params.get('date', None) is None:
    #         return APIException(detail='Query parameter "date" and "dormitory" must be included.', code=400)
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

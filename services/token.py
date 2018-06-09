from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from services.serializers import UserSerializer


class ObtainAuthTokenAndUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = User.objects.get(id=token.user_id)
        serializer = UserSerializer(user)

        return Response({
            'token': token.key,
            'user': serializer.data
        })

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from services.models import User, WashingSchedule, WashingTime


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password",
                  "date_joined")

    def create(self, validated_data):
        """
        Delete confirm_password field and create
        hash of password before model is created.
        """
        del validated_data["confirm_password"]
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def validate(self, attrs):
        """
        Check if the passwords match and causes
        an error if this is not the case.
        """
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return attrs


class WashingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingTime
        fields = "__all__"

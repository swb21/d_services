from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from services.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('fullname', 'phone_number', 'dormitory', 'room')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password", "is_staff", "profile")

    def create(self, validated_data):
        """
        Delete confirm_password field and create
        hash of password before model is created.
        """
        del validated_data["confirm_password"]
        validated_data["password"] = make_password(validated_data["password"])

        profile_data = validated_data.pop('profile')

        user = User.objects.create(**validated_data)
        profile, created = Profile.objects.update_or_create(
            user=user,
            defaults=profile_data,
        )

        return profile.user

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
        fields = ('id', 'time')


class WashingMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingMachine
        fields = ('id', 'number')


class WashingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingSchedule
        fields = "__all__"


class DormitorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormitory
        fields = ('id', 'number', 'address')

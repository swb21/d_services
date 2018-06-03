from django.contrib import admin

from services.models import Dormitory, Profile, Staff, StaffRequest, WashingMachine, WashingSchedule


@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    model = Dormitory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    model = Staff


@admin.register(StaffRequest)
class StaffRequestAdmin(admin.ModelAdmin):
    model = StaffRequest


@admin.register(WashingMachine)
class WashingMachineAdmin(admin.ModelAdmin):
    model = WashingMachine


@admin.register(WashingSchedule)
class WashingScheduleAdmin(admin.ModelAdmin):
    model = WashingSchedule

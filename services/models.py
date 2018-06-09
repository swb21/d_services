from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=
    _("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed"
      ))


class Dormitory(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    address = models.CharField(max_length=80)
    commandant_phone = models.CharField(
        validators=[phone_validator], max_length=17, null=True, blank=True)

    class Meta:
        verbose_name = _('Dormitory')
        verbose_name_plural = _('Dormitories')
        ordering = ['number']

    def __str__(self):
        return "{}, {}".format(self.number, self.address)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    fullname = models.CharField(max_length=90)
    dormitory = models.ForeignKey(
        Dormitory, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.CharField(max_length=5, null=True, blank=True)

    phone_number = models.CharField(
        validators=[phone_validator], max_length=17, null=True, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return "{}, {}".format(self.fullname or 'No name', self.phone_number
                               or 'No phone number')


class Staff(models.Model):
    working_position = models.CharField(max_length=20)
    starts_working_at = models.TimeField(null=True, blank=True)
    ends_working_at = models.TimeField(null=True, blank=True)
    works_on_weekend = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Staff')

    def __str__(self):
        return "{}, {}".format(self.user.profile.fullname or 'No name',
                               self.working_position)


class StaffRequest(models.Model):
    description = models.TextField()
    desired_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)

    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Staff request')
        verbose_name_plural = _('Staff requests')

    def __str__(self):
        return "Who: {}, to whom: {}".format(self.user.profile.fullname,
                                             self.staff.working_position)


class WashingMachine(models.Model):
    EXPLOITABLE = True
    NOT_EXPLOITABLE = False

    EXPLOITABLE_CHOICES = (
        (EXPLOITABLE, _('Exploitable')),
        (NOT_EXPLOITABLE, _('Not exploitable')),
    )

    number = models.PositiveSmallIntegerField()
    is_exploitable = models.BooleanField(
        choices=EXPLOITABLE_CHOICES, default=EXPLOITABLE)

    dormitory = models.ForeignKey(
        Dormitory, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Washing machine')
        verbose_name_plural = _('Washing machines')
        ordering = ['-is_exploitable', 'dormitory__number', 'number']

    def __str__(self):
        return "Dormitory {}, washing machine {} ({}) ".format(
            self.dormitory.number, self.number,
            self.get_is_exploitable_display())


class WashingTime(models.Model):
    time = models.TimeField()

    class Meta:
        verbose_name = _('Washing time')
        verbose_name_plural = _('Washing time')
        ordering = ['time']

    def __str__(self):
        return "{}".format(self.time)


class WashingSchedule(models.Model):
    washing_machine = models.ForeignKey(
        WashingMachine, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.ForeignKey(WashingTime, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Washing schedule')
        verbose_name_plural = _('Washing schedules')
        ordering = ['date', 'time', 'washing_machine']
        unique_together = (('user', 'date'), )

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):

        super(WashingSchedule, self).save(
            self, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return "When: {} {}, dormitory/washing machine: {}/{}".format(
            self.date, self.time.time, self.washing_machine.dormitory.number,
            self.washing_machine.number)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

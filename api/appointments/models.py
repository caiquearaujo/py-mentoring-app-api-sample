from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from metadata.models import Metadata
from users.models import User


class AppointmentManager(models.BaseManager):
    use_in_migrations = True

    def get_by_id(self, id: int):
        return self.get(id=id)

    def get_by_both(self, member: User, mentor: User):
        return self.filter(member=member, mentor=mentor)

    def get_by_member(self, member: User):
        return self.filter(member=member)

    def get_by_mentor(self, mentor: User):
        return self.filter(mentor=mentor)


class AppointmentStatus(models.IntegerChoices):
    SCHEDULED = 1, _("Scheduled")
    CANCELED = 2, _("Canceled")
    CONCLUDED = 3, _("Concluded")


# Create your models here.
class Appointment(models.Model):
    member = models.OneToOneField(
        User,
        verbose_name=_("Member"),
        on_delete=models.CASCADE,
        related_name="member_id",
        db_index=True,
    )

    mentor = models.OneToOneField(
        User,
        verbose_name=_("Mentor"),
        on_delete=models.CASCADE,
        related_name="mentor_id",
        db_index=True,
    )

    mentorship_area = models.OneToOneField(
        Metadata,
        verbose_name=_("Mentorship"),
        on_delete=models.SET_NULL,
        related_name="mentorship_area_id",
        null=True,
        db_index=True,
    )

    expertise = models.OneToOneField(
        Metadata,
        verbose_name=_("Expertise"),
        on_delete=models.SET_NULL,
        related_name="expertise_id",
        null=True,
        db_index=True,
    )

    start_time = models.DateTimeField(
        verbose_name=_("Start time"),
        blank=False,
        null=False,
        db_index=True,
    )

    end_time_expected = models.DateTimeField(
        verbose_name=_("Expected end time"),
        blank=False,
        null=False,
        db_index=True,
    )

    end_time = models.DateTimeField(
        verbose_name=_("End time"),
        blank=True,
        null=True,
        default=None,
        db_index=True,
    )

    status = models.PositiveSmallIntegerField(
        verbose_name=_("Status"),
        choices=AppointmentStatus.choices,
        blank=False,
        null=False,
        db_index=True,
    )

    date_created = models.DateTimeField(
        verbose_name=_("Date of Creation"),
        default=timezone.now,
        db_index=True,
    )

    objects = AppointmentManager()

    class Meta:
        db_table = "appointments"
        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=AppointmentStatus.values),
                name="valid_appointment_status",
            )
        ]

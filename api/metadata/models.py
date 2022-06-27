from django.db import models
from django.utils.translation import gettext_lazy as _


class MetadataKey(models.TextChoices):
    EXPERTISE = "expertise", _("Expertise")
    MEMBERSHIP_AREA = "membership_area", _("Membership Area")


class MetadataManager(models.Manager):
    use_in_migrations = True

    def get_by_key(self, key):
        return self.get(key=key)


class Metadata(models.Model):
    key = models.CharField(
        max_length=25,
        verbose_name=_("Key to Metadata"),
        choices=MetadataKey.choices,
        blank=False,
        null=False,
        db_index=True,
    )

    value = models.CharField(
        verbose_name=_("Value to Metadata"),
        max_length=255,
    )

    objects = MetadataManager()

    class Meta:
        db_table = "metadatas"
        constraints = [
            models.CheckConstraint(
                check=models.Q(key__in=MetadataKey.values),
                name="valid_key",
            )
        ]

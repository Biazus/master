from django.db import models
from profiles.models import Organization


class Analysis(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name="Organization",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    raw_file = models.FileField(upload_to='uploads/')

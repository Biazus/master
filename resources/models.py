from django.db import models


class Resource(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    open_source = models.BooleanField(default=False)
    collaborative = models.BooleanField(default=False)
    available_web = models.BooleanField(default=False)
    multiplatform = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ResourceType(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

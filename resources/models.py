from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30,)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

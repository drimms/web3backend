from django.db import models


class Lead(models.Model):
    hashname = models.CharField(max_length=300)
    typeaction = models.CharField(max_length=300)
    summ = models.DecimalField(decimal_places=10, max_digits=10)

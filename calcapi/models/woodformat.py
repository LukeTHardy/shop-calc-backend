from django.db import models

class WoodFormat(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
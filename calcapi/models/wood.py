from django.db import models

class Wood(models.Model):
    species = models.CharField(max_length=500, null=True, blank=True)
    domestic = models.BooleanField(default=True)
    hardwood = models.BooleanField(default=True)
    density = models.FloatField(null=True)
    origin = models.CharField(max_length=500, null=True, blank=True)
    appearance = models.CharField(max_length=500, null=True, blank=True)
    characteristics = models.CharField(max_length=500, null=True, blank=True)
    colorCat = models.ForeignKey("ColorCategory", on_delete=models.CASCADE, related_name='woods_of_this_colorCat')

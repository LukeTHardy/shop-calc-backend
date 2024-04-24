from django.db import models
from django.core.validators import FileExtensionValidator


class Wood(models.Model):
    species = models.CharField(max_length=500, null=True, blank=True)
    domestic = models.BooleanField(default=True)
    hardwood = models.BooleanField(default=True)
    density = models.IntegerField(null=True)
    origin = models.CharField(max_length=500, null=True, blank=True)
    appearance = models.CharField(max_length=500, null=True, blank=True)
    characteristics = models.CharField(max_length=500, null=True, blank=True)
    colorCat = models.ForeignKey("ColorCategory", on_delete=models.CASCADE, related_name='woods_of_this_colorCat')
    image = models.ImageField(upload_to='images/woods',
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])]
    )

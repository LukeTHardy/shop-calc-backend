from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_added_by_this_user')
    species = models.ForeignKey("Wood", on_delete=models.CASCADE, related_name='inventory_of_this_wood_species', default=1)
    format = models.ForeignKey("WoodFormat", on_delete=models.CASCADE, related_name='inventory_of_this_format')
    entry_date = models.DateTimeField("date entered/updated", default=timezone.now)
    quantity = models.IntegerField(null=True)
    length = models.FloatField(null=True)
    width = models.FloatField(null=True)
    thickness = models.FloatField(null=True)
    totalBF = models.FloatField(null=True)
    notes = models.CharField(max_length=500, null=True, blank=True)

@receiver(post_save, sender=Inventory)
def calculate_totalBF(sender, instance, created, **kwargs):
    if created:
        if instance.length is not None and instance.width is not None and instance.thickness is not None and instance.quantity is not None:
            instance.totalBF = round((instance.length * instance.width * instance.thickness * instance.quantity) / 144, 2)
            instance.save()
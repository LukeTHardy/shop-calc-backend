from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

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
from django.db import models
from django.contrib.auth.models import User

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_added_by_this_user')
    wood = models.ForeignKey("Wood", on_delete=models.CASCADE, related_name='inventory_of_this_wood_type')
    format = models.ForeignKey("WoodFormat", on_delete=models.CASCADE, related_name='inventory_of_this_format')
    entry_date = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    thickness = models.IntegerField(null=True)
    totalBF = models.IntegerField(null=True)
# Generated by Django 5.0.4 on 2024-04-30 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcapi', '0004_remove_inventory_wood_inventory_species'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date entered/updated'),
        ),
    ]
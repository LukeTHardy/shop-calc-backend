# Generated by Django 5.0.4 on 2024-04-30 18:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcapi', '0006_alter_inventory_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='entry_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date entered/updated'),
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-30 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcapi', '0005_alter_inventory_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='date entered/updated'),
        ),
    ]

# Generated by Django 2.0.2 on 2018-05-03 10:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0042_auto_20180503_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrisk',
            name='probability',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]

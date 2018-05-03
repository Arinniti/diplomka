# Generated by Django 2.0.2 on 2018-05-03 10:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0040_auto_20180503_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='task',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.0)]),
        ),
    ]

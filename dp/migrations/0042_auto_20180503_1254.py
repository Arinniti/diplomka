# Generated by Django 2.0.2 on 2018-05-03 10:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0041_auto_20180503_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrisk',
            name='probability',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='projectrisk',
            name='risk_impact',
            field=models.CharField(choices=[('1', 'Insignificant'), ('2', 'Minor'), ('3', 'Important'), ('4', 'Major'), ('5', 'Catastrophic')], max_length=1, null=True),
        ),
    ]

# Generated by Django 2.0.2 on 2018-04-19 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0029_auto_20180418_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=15, null=True),
        ),
    ]

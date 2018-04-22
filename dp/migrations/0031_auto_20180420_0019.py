# Generated by Django 2.0.2 on 2018-04-19 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0030_auto_20180420_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='budget',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='used_budget',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='used_budget',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]

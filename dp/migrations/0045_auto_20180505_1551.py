# Generated by Django 2.0.2 on 2018-05-05 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0044_remove_projectrisk_risk_appetite'),
    ]

    operations = [
        migrations.AddField(
            model_name='risk',
            name='consequence',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='projectrisk',
            name='probability',
            field=models.CharField(choices=[('1', 'Very low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very high')], max_length=1, null=True),
        ),
    ]

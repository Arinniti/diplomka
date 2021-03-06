# Generated by Django 2.0.2 on 2018-05-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0058_remove_projectrisk_risk_has_impact_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='complexity',
            field=models.CharField(choices=[('1', 'High'), ('0', 'Low')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='importance',
            field=models.CharField(choices=[('1', 'High '), ('0', 'Low')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='urgency',
            field=models.CharField(choices=[('1', 'High '), ('0', 'Low')], max_length=1, null=True),
        ),
    ]

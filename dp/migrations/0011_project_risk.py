# Generated by Django 2.0.2 on 2018-04-08 17:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0010_auto_20180328_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='risk',
            field=models.CharField(choices=[('0.25', 'Small'), ('0.50', 'Medium'), ('0.75', 'Large')], default=django.utils.timezone.now, max_length=1),
            preserve_default=False,
        ),
    ]
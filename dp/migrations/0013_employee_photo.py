# Generated by Django 2.0.2 on 2018-04-08 18:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0012_auto_20180408_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='photo',
            field=models.FileField(default=django.utils.timezone.now, upload_to='photos/'),
            preserve_default=False,
        ),
    ]

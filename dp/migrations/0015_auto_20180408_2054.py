# Generated by Django 2.0.2 on 2018-04-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0014_auto_20180408_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.FileField(null=True, upload_to='dp/static/photos/'),
        ),
    ]
# Generated by Django 2.0.2 on 2018-04-08 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0016_auto_20180408_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
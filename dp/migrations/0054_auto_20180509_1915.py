# Generated by Django 2.0.2 on 2018-05-09 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0053_auto_20180509_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberability',
            name='experience',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], null=True),
        ),
    ]
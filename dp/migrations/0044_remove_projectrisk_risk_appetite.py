# Generated by Django 2.0.2 on 2018-05-03 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0043_auto_20180503_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectrisk',
            name='risk_appetite',
        ),
    ]

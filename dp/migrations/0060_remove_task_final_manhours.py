# Generated by Django 2.0.2 on 2018-05-10 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0059_auto_20180510_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='final_manhours',
        ),
    ]

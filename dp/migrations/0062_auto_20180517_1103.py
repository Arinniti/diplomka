# Generated by Django 2.0.2 on 2018-05-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0061_keyword'),
    ]

    operations = [
        migrations.DeleteModel(
            name='KeyWord',
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='date of start'),
        ),
    ]
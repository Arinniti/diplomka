# Generated by Django 2.0.2 on 2018-05-21 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0062_auto_20180517_1103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costumer',
            name='project',
        ),
        migrations.RemoveField(
            model_name='costumer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='projectnotes',
            name='author',
        ),
        migrations.RemoveField(
            model_name='projectnotes',
            name='project',
        ),
        migrations.RemoveField(
            model_name='tasknotes',
            name='author',
        ),
        migrations.RemoveField(
            model_name='tasknotes',
            name='task',
        ),
        migrations.DeleteModel(
            name='Costumer',
        ),
        migrations.DeleteModel(
            name='ProjectNotes',
        ),
        migrations.DeleteModel(
            name='TaskNotes',
        ),
    ]

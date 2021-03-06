# Generated by Django 2.0.2 on 2018-04-18 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0028_auto_20180418_2037'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assignedtask',
            unique_together={('employee', 'task')},
        ),
        migrations.AlterUniqueTogether(
            name='memberability',
            unique_together={('member', 'ability')},
        ),
        migrations.AlterUniqueTogether(
            name='projectmember',
            unique_together={('project', 'member')},
        ),
    ]

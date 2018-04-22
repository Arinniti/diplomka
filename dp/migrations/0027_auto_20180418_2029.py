# Generated by Django 2.0.2 on 2018-04-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0026_auto_20180417_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.CharField(choices=[('1', 'Planned'), ('2', 'Ongoing'), ('3', 'Finished'), ('4', 'Interrupted')], default=1, max_length=1),
        ),
    ]

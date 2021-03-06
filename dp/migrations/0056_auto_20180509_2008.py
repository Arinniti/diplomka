# Generated by Django 2.0.2 on 2018-05-09 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0055_auto_20180509_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='key_word',
        ),
        migrations.RemoveField(
            model_name='project',
            name='strategy',
        ),
        migrations.AddField(
            model_name='projectstrategy',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dp.Project'),
        ),
        migrations.AddField(
            model_name='projectstrategy',
            name='strategy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dp.Strategy'),
        ),
        migrations.AlterUniqueTogether(
            name='projectstrategy',
            unique_together={('project', 'strategy')},
        ),
    ]

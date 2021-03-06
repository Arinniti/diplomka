# Generated by Django 2.0.2 on 2018-03-27 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0007_auto_20180327_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dp.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='project_manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dp.Employee'),
        ),
        migrations.AddField(
            model_name='projectmember',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dp.Project'),
        ),
    ]

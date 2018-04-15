# Generated by Django 2.0.2 on 2018-04-11 20:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0020_auto_20180409_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MemberAbility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.FloatField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('ability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dp.Ability')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dp.Employee')),
            ],
        ),
    ]
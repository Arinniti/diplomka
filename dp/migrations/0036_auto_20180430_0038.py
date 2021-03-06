# Generated by Django 2.0.2 on 2018-04-29 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dp', '0035_auto_20180422_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='budget',
            new_name='manhours',
        ),
        migrations.AddField(
            model_name='project',
            name='complexity',
            field=models.CharField(choices=[('1', 'Complicated'), ('0', 'Easy')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='plan_budget',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='risk_type',
            field=models.CharField(choices=[('0', 'project'), ('1', 'portfolio')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('1', 'Public'), ('2', 'Private'), ('3', 'Mixed')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='final_manhours',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='projectnotes',
            name='author',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='dp.Employee'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tasknotes',
            name='author',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='dp.Employee'),
            preserve_default=False,
        ),
    ]

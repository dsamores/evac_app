# Generated by Django 2.0.7 on 2018-08-21 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0004_evacuser_seen_tutorial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evacuser',
            name='floor',
            field=models.IntegerField(blank=True, choices=[(0, 'Ground floor'), (1, '1'), (2, '2'), (3, '3')], null=True),
        ),
        migrations.AddField(
            model_name='evacuser',
            name='mobility_restriction',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='evacuser',
            name='phone_use',
            field=models.CharField(blank=True, max_length=31, null=True),
        ),
        migrations.AlterField(
            model_name='evacuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=15, null=True),
        ),
    ]

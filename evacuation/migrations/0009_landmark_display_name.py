# Generated by Django 2.0.7 on 2018-09-06 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0008_landmark_floor'),
    ]

    operations = [
        migrations.AddField(
            model_name='landmark',
            name='display_name',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
    ]

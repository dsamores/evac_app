# Generated by Django 2.0.7 on 2018-09-17 19:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0011_landmark_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

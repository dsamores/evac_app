# Generated by Django 2.0.7 on 2018-09-06 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0009_landmark_display_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='landmark',
            old_name='image',
            new_name='icon',
        ),
    ]
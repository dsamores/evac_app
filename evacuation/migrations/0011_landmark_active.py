# Generated by Django 2.0.7 on 2018-09-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0010_auto_20180906_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='landmark',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

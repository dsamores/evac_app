# Generated by Django 2.0.7 on 2018-09-18 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_auto_20180908_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=True),
        ),
    ]

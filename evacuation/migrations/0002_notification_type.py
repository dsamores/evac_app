# Generated by Django 2.0.7 on 2018-07-31 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
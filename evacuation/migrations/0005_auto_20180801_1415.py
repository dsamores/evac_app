# Generated by Django 2.0.7 on 2018-08-01 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacuation', '0004_auto_20180801_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('Alert', 'Alert'), ('Warning', 'Warning'), ('Info', 'Info'), ('Success', 'Success')], default='Alert', max_length=20),
        ),
    ]

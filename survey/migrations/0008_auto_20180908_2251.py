# Generated by Django 2.0.7 on 2018-09-08 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20180908_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=127),
        ),
        migrations.AlterField(
            model_name='choicegroup',
            name='name',
            field=models.CharField(max_length=127),
        ),
        migrations.AlterField(
            model_name='survey',
            name='name',
            field=models.CharField(max_length=127),
        ),
    ]
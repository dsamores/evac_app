# Generated by Django 2.0.7 on 2018-09-07 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20180906_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('Text', 'Text'), ('SingleChoice', 'SingleChoice'), ('SingleChoiceOther', 'SingleChoiceOther'), ('MultipleChoice', 'MultipleChoice'), ('MultipleChoiceOther', 'MultipleChoiceOther')], default='Text', max_length=31),
        ),
    ]

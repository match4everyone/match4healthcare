# Generated by Django 3.0.4 on 2020-03-30 02:20

from django.db import migrations, models

import apps.iamstudent.models


class Migration(migrations.Migration):

    dependencies = [
        ('iamstudent', '0004_merge_20200330_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='einwilligung_agb',
            field=models.BooleanField(default=False, validators=[apps.iamstudent.models.validate_checkbox]),
        ),
    ]

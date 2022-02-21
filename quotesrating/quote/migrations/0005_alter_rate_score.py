# Generated by Django 4.0.2 on 2022-02-21 16:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0004_rate_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
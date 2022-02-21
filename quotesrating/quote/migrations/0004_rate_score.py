# Generated by Django 4.0.2 on 2022-02-21 16:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0003_alter_quote_average_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
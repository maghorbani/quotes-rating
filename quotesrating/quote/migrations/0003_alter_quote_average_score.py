# Generated by Django 4.0.2 on 2022-02-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0002_alter_rate_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='average_score',
            field=models.FloatField(default=0),
        ),
    ]
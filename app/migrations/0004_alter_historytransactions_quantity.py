# Generated by Django 3.2.3 on 2021-06-01 22:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_historytransactions_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historytransactions',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]

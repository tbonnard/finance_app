# Generated by Django 3.2.3 on 2021-06-01 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_historytransactions_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='historytransactions',
            name='total_price_transaction',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historytransactions',
            name='unit_price_transaction',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

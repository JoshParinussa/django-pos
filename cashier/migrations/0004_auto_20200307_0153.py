# Generated by Django 3.0.4 on 2020-03-07 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0003_auto_20200305_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='convertbarang',
            name='grosir_1_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='convertbarang',
            name='grosir_2_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='convertbarang',
            name='grosir_3_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='convertbarang',
            name='purchase_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
    ]

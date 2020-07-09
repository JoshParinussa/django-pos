# Generated by Django 3.0.5 on 2020-07-09 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0015_purchase_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='grosir_1',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='grosir_2',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='grosir_3',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
    ]
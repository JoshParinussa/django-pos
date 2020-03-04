# Generated by Django 3.0.3 on 2020-03-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='grosir_1_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='grosir_2_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='grosir_3_price',
            field=models.DecimalField(decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_grosir_1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_grosir_2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_grosir_3',
            field=models.IntegerField(null=True),
        ),
    ]

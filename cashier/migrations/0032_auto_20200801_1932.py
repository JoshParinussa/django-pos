# Generated by Django 3.0.5 on 2020-08-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0031_auto_20200801_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='grosir_1',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='grosir_2',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='grosir_3',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True),
        ),
    ]
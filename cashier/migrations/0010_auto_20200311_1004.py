# Generated by Django 3.0.3 on 2020-03-11 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0009_invoice_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cash',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='change',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True),
        ),
    ]

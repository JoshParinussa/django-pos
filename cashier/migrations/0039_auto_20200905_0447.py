# Generated by Django 3.0.5 on 2020-09-05 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0038_auto_20200905_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='payment_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Debt'), (1, 'Cash')], db_index=True, default=1),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Onprocess'), (1, 'Success'), (3, 'Cancel')], db_index=True, default=0),
        ),
    ]
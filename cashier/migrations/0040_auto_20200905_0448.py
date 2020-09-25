# Generated by Django 3.0.5 on 2020-09-05 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0039_auto_20200905_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Onprocess'), (1, 'Success'), (2, 'Cancel')], db_index=True, default=0),
        ),
    ]
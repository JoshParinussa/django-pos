# Generated by Django 3.0.5 on 2020-06-15 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0012_merge_20200615_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='cost',
            new_name='jumlah_pemasukan',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='information',
            new_name='keterangan',
        ),
    ]

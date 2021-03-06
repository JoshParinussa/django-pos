# Generated by Django 3.0.3 on 2020-03-24 03:58

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invoice', models.CharField(db_index=True, max_length=128)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cash', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('change', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Empty'), (1, 'Success'), (2, 'Cancel')], db_index=True, default=0)),
                ('cashier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_cashier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pembayaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tgl_pembayaran', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=0, max_digits=9)),
                ('pegawai', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('barcode', models.CharField(max_length=128)),
                ('stock', models.PositiveIntegerField(blank=True, null=True)),
                ('purchase_price', models.DecimalField(decimal_places=0, max_digits=9, null=True)),
                ('selling_price', models.DecimalField(decimal_places=0, max_digits=9, null=True)),
                ('quantity_grosir_1', models.IntegerField(blank=True, null=True)),
                ('grosir_1_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('quantity_grosir_2', models.IntegerField(blank=True, null=True)),
                ('grosir_2_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('quantity_grosir_3', models.IntegerField(blank=True, null=True)),
                ('grosir_3_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(db_index=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company_name', models.CharField(db_index=True, max_length=128)),
                ('address', models.CharField(db_index=True, max_length=128)),
                ('contact_person', models.CharField(db_index=True, max_length=128)),
                ('office_phone', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(db_index=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('qty', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=0, max_digits=9)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_sale', to='cashier.Invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sale', to='cashier.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashier.ProductCategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.Supplier'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.Unit'),
        ),
        migrations.CreateModel(
            name='PembayaranProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=0, max_digits=9)),
                ('pembayaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashier.Pembayaran')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashier.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='pembayaran',
            name='products',
            field=models.ManyToManyField(through='cashier.PembayaranProduct', to='cashier.Product'),
        ),
        migrations.CreateModel(
            name='HargaBertingkat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('selling_price', models.DecimalField(decimal_places=0, max_digits=9, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashier.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConvertBarang',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=0, max_digits=9, null=True)),
                ('selling_price', models.DecimalField(decimal_places=0, max_digits=9, null=True)),
                ('grosir_1_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('grosir_2_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('grosir_3_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='convert_barang', to='cashier.Product')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.Unit')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

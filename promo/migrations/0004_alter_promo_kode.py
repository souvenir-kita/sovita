# Generated by Django 5.1.2 on 2024-10-24 14:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0003_alter_promo_kode_alter_promo_nama'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='kode',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]

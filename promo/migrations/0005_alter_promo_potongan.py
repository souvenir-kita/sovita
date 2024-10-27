# Generated by Django 5.1.2 on 2024-10-27 12:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0004_alter_promo_kode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='potongan',
            field=models.IntegerField(max_length=100, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
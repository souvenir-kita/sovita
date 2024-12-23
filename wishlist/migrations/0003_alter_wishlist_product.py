# Generated by Django 5.1.2 on 2024-10-27 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminview', '0001_initial'),
        ('wishlist', '0002_alter_wishlist_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to='adminview.product'),
        ),
    ]

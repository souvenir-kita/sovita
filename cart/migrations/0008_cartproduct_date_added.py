# Generated by Django 5.1.2 on 2024-10-27 09:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_cartproduct_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

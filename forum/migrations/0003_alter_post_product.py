# Generated by Django 5.1.2 on 2024-10-26 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminview', '0001_initial'),
        ('forum', '0002_post_product_post_user_reply_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminview.product'),
        ),
    ]

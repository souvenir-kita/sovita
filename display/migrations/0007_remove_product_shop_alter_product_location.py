# Generated by Django 5.1.2 on 2024-10-25 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0006_alter_product_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shop',
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.CharField(max_length=511),
        ),
    ]
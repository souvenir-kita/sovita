# Generated by Django 5.1.2 on 2024-10-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cartproduct_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='note',
            field=models.TextField(blank=True, max_length=144, null=True),
        ),
    ]

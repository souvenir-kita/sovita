# Generated by Django 5.1.2 on 2024-10-22 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0004_alter_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
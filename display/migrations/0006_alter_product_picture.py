# Generated by Django 5.1.2 on 2024-10-23 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0005_alter_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, default='/images/default.png', null=True, upload_to='images/'),
        ),
    ]

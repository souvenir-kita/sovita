# Generated by Django 5.1.2 on 2024-10-19 17:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('description', models.TextField()),
                ('picture', models.ImageField(default='static/img/default.png', upload_to='static/img/')),
                ('location', models.CharField(max_length=255)),
                ('shop', models.CharField(max_length=255)),
            ],
        ),
    ]
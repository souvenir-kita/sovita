# Generated by Django 5.1.2 on 2024-10-27 06:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_alter_reviewentry_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewentry',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]

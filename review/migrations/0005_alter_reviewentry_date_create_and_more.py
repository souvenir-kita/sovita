# Generated by Django 5.1.2 on 2024-10-27 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_alter_reviewentry_date_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewentry',
            name='date_create',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reviewentry',
            name='date_update',
            field=models.DateField(auto_now=True),
        ),
    ]

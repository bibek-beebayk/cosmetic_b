# Generated by Django 5.0 on 2025-07-14 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0003_service_service_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="image",
            field=models.ImageField(max_length=1000, upload_to="services/"),
        ),
    ]

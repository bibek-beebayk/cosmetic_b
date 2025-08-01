# Generated by Django 5.0 on 2025-07-14 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0004_alter_service_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="image",
            field=models.ImageField(max_length=1000, upload_to="staff/"),
        ),
        migrations.AlterField(
            model_name="staff",
            name="services",
            field=models.ManyToManyField(related_name="staffs", to="service.service"),
        ),
    ]

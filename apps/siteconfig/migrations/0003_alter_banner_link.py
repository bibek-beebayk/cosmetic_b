# Generated by Django 5.2.3 on 2025-07-01 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0002_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Banner Link'),
        ),
    ]

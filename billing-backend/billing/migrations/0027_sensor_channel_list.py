# Generated by Django 4.1.6 on 2023-03-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0026_rename_sensor_sensor_sensor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='channel_list',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.1.6 on 2023-02-16 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_alter_subscription_service_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='poc',
        ),
    ]
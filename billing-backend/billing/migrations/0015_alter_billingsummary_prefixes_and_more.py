# Generated by Django 4.1.6 on 2023-02-22 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_alter_billingsummary_prefixes_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingsummary',
            name='prefixes',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='billingsummary',
            name='prefixes_done',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

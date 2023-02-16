# Generated by Django 4.1.6 on 2023-02-16 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_alter_subscription_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='product',
            field=models.CharField(choices=[('uCDN Production', 'uCDN Production'), ('H7Connect-DC', 'H7Connect-DC'), ('H7Connect-IX', 'H7Connect-IX'), ('H7Connect-CHINA IP', 'H7Connect-CHINA IP'), ('H7Connect-VC', 'H7Connect-VC'), ('uCDN POC', 'uCDN POC'), ('Infrastructure', 'Infrastructure')], default='uCDN', max_length=100, verbose_name='Product name'),
        ),
    ]

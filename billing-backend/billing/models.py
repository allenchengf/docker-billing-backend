from django.db import models


class Customer(models.Model):

    PROPERTY_CHOICES = (
        ('Presales', 'Presales'),
        ('Existing', 'Existing'),
        ('Terminated', 'Terminated')
    )

    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, unique=True)
    customer_property = models.CharField(verbose_name="Task status", max_length=20, choices=PROPERTY_CHOICES, default='Presales')
    am = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.customer_id


class Subscription(models.Model):

    PRODUCT_CHOICES = (
        ('uCDN', 'uCDN'),
        ('H7Connect-DC', 'H7Connect-DC'),
        ('H7Connect-IX', 'H7Connect-IX'),
        ('H7Connect-CHINA IP', 'H7Connect-CHINA IP'),
        ('H7Connect-VC', 'H7Connect-VC'),
        ('uCDN POC', 'uCDN POC'),
        ('Infrastructure', 'Infrastructure'),
    )

    customer_id = models.IntegerField(null=False)
    product = models.CharField(verbose_name="Product name", max_length=100, choices=PRODUCT_CHOICES, default='uCDN')
    service_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    poc = models.CharField(max_length=50, default='Production')
    status = models.CharField(max_length=20, default='In Use')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.service_id

from django.db import models


class Customer(models.Model):
    PROPERTY_CHOICES = (
        ('Presales', 'Presales'),
        ('Existing', 'Existing'),
        ('Terminated', 'Terminated')
    )

    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, unique=True)
    customer_property = models.CharField(verbose_name="Task status", max_length=20, choices=PROPERTY_CHOICES,
                                         default='Presales')
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
    status = models.CharField(max_length=20, default='In Use')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.service_id


class BillingSummary(models.Model):
    billing_id = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    service_id = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    month = models.CharField(max_length=255, blank=True, null=True)
    percentile_98_h = models.IntegerField(blank=True, null=True)
    percentile_98_hm = models.IntegerField(blank=True, null=True)
    percentile_98 = models.IntegerField(blank=True, null=True)
    percentile_98_m = models.IntegerField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    prefixes = models.JSONField(blank=True, null=True)
    cir = models.IntegerField(blank=True, null=True)
    pir = models.IntegerField(blank=True, null=True)
    percentile_mbps_98 = models.IntegerField(blank=True, null=True)
    fqdn_subscribed = models.TextField(blank=True, null=True)
    fqdn_additional = models.TextField(blank=True, null=True)
    pricing = models.CharField(max_length=255, blank=True, null=True)
    prefixes_done = models.JSONField(blank=True, null=True, )
    monthly_report_done = models.IntegerField(blank=True, null=True, default=0)
    order = models.CharField(max_length=255, blank=True, null=True)
    sales_tag = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class BillingSummaryAggregates(models.Model):
    group_name = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    month = models.CharField(max_length=255, blank=True, null=True)
    billing_list = models.JSONField(blank=True, null=True)
    percentile_98_h = models.IntegerField(blank=True, null=True)
    percentile_98_hm = models.IntegerField(blank=True, null=True)
    percentile_98 = models.IntegerField(blank=True, null=True)
    percentile_98_m = models.IntegerField(blank=True, null=True)
    percentile_mbps_98 = models.IntegerField(blank=True, null=True)
    data_progress = models.CharField(max_length=255, blank=True, null=True)
    monthly_report_done = models.IntegerField(blank=True, null=True, default=0)
    sequence = models.IntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class BillingSetting(models.Model):
    customer_id = models.IntegerField(null=False)
    service_id = models.IntegerField(null=False)
    billing_id = models.CharField(max_length=255, null=False)
    cir = models.IntegerField(blank=True, null=True)
    pir = models.IntegerField(blank=True, null=True)
    provisioned_at = models.CharField(max_length=255, blank=True, null=True)
    terminated_at = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.billing_id


class BillingSettingAggregates(models.Model):
    group_name = models.CharField(max_length=255, null=True)
    billing_list = models.JSONField(blank=True, null=True)
    cir = models.IntegerField(blank=True, null=True)
    pir = models.IntegerField(blank=True, null=True)
    permanent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.group_name


class Sensor(models.Model):
    billing_settings = models.ForeignKey(BillingSetting, related_name='sensors', blank=True, null=True, on_delete=models.CASCADE)
    sensor_id = models.IntegerField(null=False)
    channel_list = models.JSONField(blank=True, null=True)
    prefix_list = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

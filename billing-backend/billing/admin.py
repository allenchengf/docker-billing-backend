from django.contrib import admin
from .models import Customer
from .models import Subscription
from .models import BillingSummary


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_id', 'created_at', 'updated_at')

    '''filter options'''
    list_filter = ('customer_id',)

    '''10 items per page'''
    list_per_page = 10


admin.site.register(Customer, CustomerAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'service_id', 'status', 'created_at', 'updated_at')

    '''filter options'''
    list_filter = ('service_id',)

    '''10 items per page'''
    list_per_page = 10


admin.site.register(Subscription, SubscriptionAdmin)


class BillingSummaryAdmin(admin.ModelAdmin):
    list_display = (
        'billing_id',
        'customer_id',
        'service_id',
        'year', 'month',
        'percentile_98_h',
        'percentile_98_hm',
        'percentile_98',
        'percentile_98_m',
        'history',
        'prefixes',
        'cir',
        'pir',
        'percentile_mbps_98',
        'fqdn_subscribed',
        'fqdn_additional',
        'pricing',
        'prefixes_done',
        'monthly_report_done',
        'order',
        'sales_tag',
        'created_at',
        'updated_at'
    )

    '''filter options'''
    list_filter = ('service_id',)

    '''10 items per page'''
    list_per_page = 10


admin.site.register(BillingSummary, BillingSummaryAdmin)

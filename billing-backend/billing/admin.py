from django.contrib import admin
from .models import Customer
from .models import Subscription


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_id', 'created_at', 'updated_at')

    '''filter options'''
    list_filter = ('customer_id',)

    '''10 items per page'''
    list_per_page = 10


admin.site.register(Customer, CustomerAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'service_id', 'poc', 'status', 'created_at', 'updated_at')

    '''filter options'''
    list_filter = ('service_id',)

    '''10 items per page'''
    list_per_page = 10


admin.site.register(Subscription, SubscriptionAdmin)

from rest_framework import serializers
from .models import Customer
from .models import Subscription
from .models import BillingSummary
from .models import BillingSummaryAggregates


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class BillingSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSummary
        fields = '__all__'


class BillingSummaryAggregatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSummaryAggregates
        fields = '__all__'
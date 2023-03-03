from rest_framework import serializers
from .models import Customer
from .models import Subscription
from .models import BillingSummary
from .models import BillingSummaryAggregates
from .models import BillingSetting
from .models import Sensor
from .models import BillingSettingAggregates


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


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class BillingSettingSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True)

    class Meta:
        model = BillingSetting
        fields = [
            'id',
            'customer_id',
            'service_id',
            'billing_id',
            'cir',
            'pir',
            'provisioned_at',
            'terminated_at',
            'sensors',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        sensors_data = validated_data.pop('sensors')
        billingSetting = BillingSetting.objects.create(**validated_data)
        for sensor_data in sensors_data:
            Sensor.objects.create(billing_settings_id=billingSetting.id, **sensor_data)

        return billingSetting

    def update(self, instance, validated_data):
        sensors_data = validated_data.pop('sensors')
        sensors = instance.sensors.all()
        sensors = list(sensors)
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.service_id = validated_data.get('service_id', instance.service_id)
        instance.billing_id = validated_data.get('billing_id', instance.billing_id)
        instance.cir = validated_data.get('cir', instance.cir)
        instance.pir = validated_data.get('pir', instance.pir)
        instance.provisioned_at = validated_data.get('provisioned_at', instance.provisioned_at)
        instance.terminated_at = validated_data.get('terminated_at', instance.terminated_at)
        instance.save()

        for sensors_data in sensors_data:
            sensor = sensors.pop(0)
            sensor.sensor_id = sensors_data.get('sensor_id', sensor.sensor_id)
            sensor.channel_list = sensors_data.get('channel_list', sensor.channel_list)
            sensor.prefix_list = sensors_data.get('prefix_list', sensor.prefix_list)
            sensor.save()
        return instance


class BillingSettingAggregatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSettingAggregates
        fields = '__all__'

    cir = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    pir = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_cir(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

    def validate_pir(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

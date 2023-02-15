from rest_framework.generics import GenericAPIView
from .models import Customer
from .models import Subscription
from .serializers import CustomerSerializer
from .serializers import SubscriptionSerializer
from django.http import JsonResponse
from django.db import transaction
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
import redis
from django.conf import settings
from rest_framework.response import Response
import json

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


class CustomersView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **krgs):
        customers = self.get_queryset()
        serializer = self.serializer_class(customers, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SubscriptionsView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **krgs):
        subscriptions = self.get_queryset()
        serializer = self.serializer_class(subscriptions, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class SensorsView(generics.GenericAPIView):
    def get(self, request, *args, **krgs):
        data = redis_instance.get('sensors_menu')
        return Response(json.loads(data))

class ChannelsView(generics.GenericAPIView):
    def get(self, request, *args, **krgs):
        data = redis_instance.get('channels_menu')
        return Response(json.loads(data))


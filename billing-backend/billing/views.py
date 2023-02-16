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
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.blacklist.models import BlacklistedToken
from rest_framework_jwt.blacklist.serializers import BlacklistTokenSerializer

# redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
#                                   port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASS)

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


class UserView(generics.GenericAPIView):
    def get(self, request, *args, **krgs):
        data = {
            "code": 20000,
            "data": {
                "roles": ["admin"],
                "introduction": "I am a rd administrator",
                 "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                 "name": "Super Admin"
            }
        }
        return JsonResponse(data)

class LogoutView(ModelViewSet):
    queryset = BlacklistedToken.objects.all()
    serializer_class = BlacklistTokenSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        if 'token' not in request.data:
            request.data.update({
                'token': JSONWebTokenAuthentication.get_token_from_request(request)
            })

        super(LogoutView, self).create(request, *args, **kwargs)

        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

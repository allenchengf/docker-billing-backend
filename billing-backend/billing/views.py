from rest_framework.generics import GenericAPIView
from .models import Customer
from .models import Subscription
from .models import BillingSummary
from .models import BillingSummaryAggregates
from .models import BillingSetting
from .models import BillingSettingAggregates
from .serializers import CustomerSerializer
from .serializers import SubscriptionSerializer
from .serializers import BillingSummarySerializer
from .serializers import BillingSummaryAggregatesSerializer
from .serializers import BillingSettingSerializer
from .serializers import BillingSettingAggregatesSerializer
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


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASS)


class CustomersView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **krgs):
        customers = self.get_queryset()
        serializer = self.serializer_class(customers, many=True)
        # data = serializer.data
        data = {
            'code': 20000,
            'data': serializer.data
        }
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            # data = serializer.data
            data = {
                'code': 20000,
                'data': serializer.data
            }
        except Exception as e:
            data = {'message': str(e)}
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)


class SubscriptionsView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **krgs):
        subscriptions = self.get_queryset()
        serializer = self.serializer_class(subscriptions, many=True)
        # data = serializer.data
        data = {
            'code': 20000,
            'data': serializer.data
        }
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            # data = serializer.data
            data = {
                'code': 20000,
                'data': serializer.data
            }
        except Exception as e:
            data = {
                'message': str(e)
            }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)


class BillingSummaryView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = BillingSummary.objects.all()
    serializer_class = BillingSummarySerializer

    def get(self, request, *args, **krgs):
        BillingSummary = self.get_queryset()
        serializer = self.serializer_class(BillingSummary, many=True)
        data = {
            'code': 20000,
            'data': serializer.data
        }
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = {
                'code': 20000,
                'data': serializer.data
            }
        except Exception as e:
            data = {
                'message': str(e)
            }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)


class BillingSummaryAggregatesView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = BillingSummaryAggregates.objects.all()
    serializer_class = BillingSummaryAggregatesSerializer

    def get(self, request, *args, **krgs):
        BillingSummaryAggregates = self.get_queryset()
        serializer = self.serializer_class(BillingSummaryAggregates, many=True)
        data = {
            'code': 20000,
            'data': serializer.data
        }
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = {
                'code': 20000,
                'data': serializer.data
            }
        except Exception as e:
            data = {
                'message': str(e)
            }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)


class BillingSettingAggregatesView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = BillingSettingAggregates.objects.all()
    serializer_class = BillingSettingAggregatesSerializer

    def get(self, request, *args, **krgs):
        BillingSettingAggregates = self.get_queryset()
        serializer = self.serializer_class(BillingSettingAggregates, many=True)
        data = {
            'code': 20000,
            'data': serializer.data
        }
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = {
                'code': 20000,
                'data': serializer.data
            }
        except Exception as e:
            data = {
                'message': str(e)
            }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)


class BillingSettingView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = BillingSetting.objects.all()
    serializer_class = BillingSettingSerializer

    def get(self, request, *args, **krgs):
        BillingSettings = self.get_queryset()
        serializer = self.serializer_class(BillingSettings, many=True)
        data = {
            'code': 20000,
            'data': serializer.data
        }
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = {
                'code': 20000,
                'data': serializer.data
            }
        except Exception as e:
            data = {
                'message': str(e)
            }
        return JsonResponse(data)


    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            "code": 20000,
            "data": 'success'
        }

        return JsonResponse(data)


class SensorsView(generics.GenericAPIView):
    def get(self, request, *args, **krgs):
        data = {
            'code': 20000,
            'data': json.loads(redis_instance.get('sensors_menu'))
        }
        return Response(data)


class ChannelsView(generics.GenericAPIView):
    def get(self, request, *args, **krgs):
        data = {
            'code': 20000,
            'data': json.loads(redis_instance.get('channels_menu'))
        }
        return Response(data)


class PrefixesView(generics.GenericAPIView):
    def get(self, request, *args, **krgs):
        data = {
            'code': 20000,
            'data': json.loads(redis_instance.get('prefixes_menu'))
        }
        return Response(data)


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

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# urlpatterns = [
#     path('customers/', views.CustomersView.as_view(), name="customers"),
# ]

# urlpatterns = [
#     re_path(r'^customers/$', views.CustomersView.as_view()),
#     re_path(r'^customers/(?P<pk>[0-9]+)$', views.CustomersView.as_view()),]

urlpatterns = [
    re_path(r'^customers/$', views.CustomersView.as_view()),
    re_path(r'^customers/(?P<pk>[0-9]+)$', views.CustomersView.as_view()),
    re_path(r'^subscriptions/$', views.SubscriptionsView.as_view()),
    re_path(r'^subscriptions/(?P<pk>[0-9]+)$', views.SubscriptionsView.as_view()),
    re_path(r'^sensors/$', views.SensorsView.as_view()),
    re_path(r'^channels/$', views.ChannelsView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

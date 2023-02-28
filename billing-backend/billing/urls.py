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
    re_path(r'^billing-summary/$', views.BillingSummaryView.as_view()),
    re_path(r'^billing-summary/(?P<pk>[0-9]+)$', views.BillingSummaryView.as_view()),
    re_path(r'^billing-summary-aggregates/$', views.BillingSummaryAggregatesView.as_view()),
    re_path(r'^billing-summary-aggregates/(?P<pk>[0-9]+)$', views.BillingSummaryAggregatesView.as_view()),
    re_path(r'^billing-settings/$', views.BillingSettingView.as_view()),
    re_path(r'^billing-settings/(?P<pk>[0-9]+)$', views.BillingSettingView.as_view()),
    re_path(r'^billing-setting-aggregates/$', views.BillingSettingAggregatesView.as_view()),
    re_path(r'^billing-setting-aggregates/(?P<pk>[0-9]+)$', views.BillingSettingAggregatesView.as_view()),
    re_path(r'^sensors/$', views.SensorsView.as_view()),
    re_path(r'^channels/$', views.ChannelsView.as_view()),
    re_path(r'^user/$', views.UserView.as_view()),
    re_path(r'^logout/$', views.LogoutView.as_view({"post": "create"})),
]

urlpatterns = format_suffix_patterns(urlpatterns)

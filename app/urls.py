from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
simple_router = SimpleRouter()
simple_router.register(r'item', views.ItemView, basename='ItemView')
simple_router.register(r'category', views.CategoryView, basename='CategoryView')
simple_router.register(r'order', views.OrderViewSet, basename='OrderViewSet')

urlpatterns = [
    url(r'^api/v1/', include(simple_router.urls)),
    path('app', views.IndexView.as_view(), name='index'),
    path('order', views.OrderView.as_view(), name='order'),
    path('order_summary', views.OrderSummaryView.as_view(), name='order-summary'),
]
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Item, Order, OrderItem, Address
from .serializers import CategorySerializer, ItemSerializer, OrderSerializer
from .utils.common_utils import CommonUtils
from .utils.sns_client import SNSClient


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderView(TemplateView):
    template_name = 'order.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class OrderSummaryView(TemplateView):
    template_name = 'order-summary.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SUper Category View
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemView(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SUper Category View
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    @action(detail=False, methods=['post'])
    def filter(self, request):
        """
        :param request:
        :return:
        """
        data = request.data
        category = data["category"]
        print(category)
        query_set = Item.objects.filter(category__id=category)
        print(query_set)
        result = self.get_serializer_class()(query_set, many=True).data
        return Response(result)

class OrderViewSet(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SUper Category View
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "readable_id"

    def create(self, request, *args, **kwargs):
        data = request.data
        items = data.pop("items")
        address = data.pop("address")
        data["shipping_address"] = Address.objects.create(**address)
        data["readable_id"] = CommonUtils.generate_booking_id()
        data["ordered_date"] = data["ordered_date"].split('T')[0]
        order_items = [OrderItem.objects.create(**item) for item in items]
        order = Order.objects.create(**data)
        order.items.set(order_items)
        order.save()
        SNSClient.send_sms(order.phone, order.name, order.readable_id)
        return Response(self.get_serializer_class()(order).data)


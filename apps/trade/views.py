from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShopCartSerializer, ShopCartDetailSerializer \
    # , OrderSerializer, OrderDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        从购物车移除f
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = "goods_id"

    # 库存数-1
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    # 库存数+1
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        # 取goods在del之前取之后就被删掉了
        instance.delete()

    # 更新库存
    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        # 先保存之前的数据existed_nums
        saved_record = serializer.save()
        # 变化的数量
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        """覆写,当GET时获取详细购物车"""
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

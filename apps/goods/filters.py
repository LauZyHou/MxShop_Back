from rest_framework import generics
from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
    """商品的过滤类"""
    # 区间查询,指定区间的最大最小值
    min_price = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # 模糊查询,这里带i是忽略大小写
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price', 'name']

from rest_framework import generics
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(filters.FilterSet):
    """商品的过滤类"""
    # 区间查询,指定区间的最大最小值
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte', help_text="最低价格")
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # 模糊查询,这里带i是忽略大小写
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    # 查询某个类目下的所有商品
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        """查询某个类目下的所有商品"""
        # 商品的id(直接在本级下),或其所属类别的父类的id(本商品在下1级下),或其所属类别的父类的父类的id(本商品在下2级下)是要找的类别id(存在value中)
        return queryset.filter(Q(category_id=value)
                               | Q(category__parent_category_id=value)
                               | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name', 'top_category', 'is_hot']

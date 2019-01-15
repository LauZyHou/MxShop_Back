from rest_framework import serializers
from .models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    """商品类别"""

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """商品"""
    # 自己定义字段去覆盖自动序列化的字段
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = "__all__"

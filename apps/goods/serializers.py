from rest_framework import serializers
from .models import Goods, GoodsCategory, HotSearchWords, GoodsImage


# ---------------------------------------------------------------

class CategorySerializer3(serializers.ModelSerializer):
    """商品三级类别序列化"""

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """商品二级类别序列化"""
    # 通过外键的related_name来找到子类
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """商品一级类别序列化"""
    # 通过外键的related_name来找到子类
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


# ---------------------------------------------------------------
class GoodsImageSerializer(serializers.ModelSerializer):
    """商品详情页左侧轮播图"""

    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    """商品序列化"""
    # 自己定义字段去覆盖自动序列化的字段
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)  # 加入轮播图(使用商品为外键,一对多)

    class Meta:
        model = Goods
        fields = "__all__"


# ---------------------------------------------------------------

class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"

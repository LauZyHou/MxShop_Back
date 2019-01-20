# encoding: utf-8
from rest_framework.validators import UniqueTogetherValidator

__author__ = 'mtianyan'
__date__ = '2018/3/10 0010 09:54'
from rest_framework import serializers
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    """收藏商品的详细信息"""
    # 通过goods_id拿到商品信息。就需要嵌套的Serializer
    goods = GoodsSerializer() # 这里为了简单就用goods的所有字段了

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    """用户收藏"""
    # 用户收藏时不指明用户,只操作自己这个用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        # 使用validate方式实现唯一联合,不允许重复收藏
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        # 这里设置id,则收藏成功后id会被返回,用id可以取消收藏
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    """用户留言"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only只返回,不提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    """用户收货地址"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")

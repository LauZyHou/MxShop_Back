from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
# Create your views here.
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
# JWT不在settings里配置,改到这种具体的view里使用
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UserFavViewset(viewsets.GenericViewSet,
                     mixins.ListModelMixin,  # 获取收藏列表
                     mixins.CreateModelMixin,  # 添加收藏
                     mixins.RetrieveModelMixin,  # 判断是否收藏了
                     mixins.DestroyModelMixin):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    # queryset = UserFav.objects.all()
    # 访问权限认证:IsAuthenticated已登录(否则401),IsOwnerOrReadOnly只能删自己的(否则404)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    # 根据goods_id来定位资源,而不再根据id,这样在删除时和查看收藏时都更加方便和合理
    lookup_field = 'goods_id'
    # lookup_field = 'goods'
    # 用户认证:JWT(用于MxShop的普通用户),Session(用于xadmin).将用户认证放到具体的view里就不会在全局做证了
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 收藏数+1
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     # 通过这个instance Userfav找到goods
    #     goods = instance.goods
    #     goods.fav_num +=1
    #     goods.save()

    def get_queryset(self):
        """重载该方法,只返回本User对应的数据"""
        return UserFav.objects.filter(user=self.request.user)

    # 设置动态的Serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer

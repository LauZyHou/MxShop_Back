from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer
from .models import Goods, GoodsCategory, HotSearchWords
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    """自定义分页,用于商品的分页"""
    # 每页多少条记录(这里应该适应前端)
    page_size = 12
    # 可以在url参数中使用'page_size='来指定上面那个page_size的值
    page_size_query_param = 'page_size'
    # 这里指定的是分页时,页面url里表明在哪一页的参数名
    page_query_param = 'page'
    max_page_size = 100


class GoodsViewSet(mixins.ListModelMixin,  # 列表(一堆有序的商品)
                   mixins.RetrieveModelMixin,  # 详情(单个商品)
                   viewsets.GenericViewSet):
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Goods.objects.all()
    # filter_fields = ('name', 'shop_price')
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')
    # 设置默认的排序规则,以用于分页
    ordering = ('id',)
    # 设置Token认证.这里改用JWT认证了,将它注解掉
    # authentication_classes = (TokenAuthentication, )


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
      商品分类列表数据
    """
    # 只要去获取第一级别的类就可以了,它序列化时序列化了子类二类,子类二类序列化时又序列化了三类
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
    # 继承了mixins.RetrieveModelMixin就可以直接用RESTful的/xxxs/id来访问到资源中的具体某一个


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")  # 降序排序
    serializer_class = HotWordsSerializer

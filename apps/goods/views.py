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

from .serializers import GoodsSerializer
from .models import Goods
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    """自定义分页,用于商品的分页"""
    # 每页多少条记录
    page_size = 10
    # 可以在url参数中使用'page_size='来指定上面那个page_size的值
    page_size_query_param = 'page_size'
    # 这里指定的是分页时,页面url里表明在哪一页的参数名
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Goods.objects.all()
    # filter_fields = ('name', 'shop_price')
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'add_time')

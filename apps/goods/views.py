from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .serializers import GoodsSerializer
from .models import Goods


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
    # 设置排序规则,这样才能在分页时没有报错
    queryset = Goods.objects.get_queryset().order_by("goods_sn")
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

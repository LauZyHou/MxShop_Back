from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from .serializers import GoodsSerializer
from .models import Goods


class GoodsListView(APIView):
    def get(self, response, format=None):
        goods = Goods.objects.all()[:10]
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # DRf的Request中数据都已经取出放在了data属性里,使用起来很方便
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            # 这里save()根据对象是否已经存在去调用create()或者update()方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

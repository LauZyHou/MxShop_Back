# encoding: utf-8
__author__ = 'mtianyan'
__date__ = '2018/3/10 0010 17:38'
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    这里用于做[收藏],[购物车]等的权限认证
    见:https://www.django-rest-framework.org/api-guide/permissions/#examples
    """

    def has_object_permission(self, request, view, obj):
        # 对于'GET', 'HEAD', 'OPTIONS'这些安全的方法直接通过权限认证
        if request.method in permissions.SAFE_METHODS:
            return True

        # 否则就要做权限认证
        # 这里这些表的外键不叫owner而是user,自己只能操作自己这个user的,所以把这里改成user
        return obj.user == request.user

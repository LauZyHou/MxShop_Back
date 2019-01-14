# -*- coding:utf-8 -*-
from django.apps import AppConfig


class UserOperationsConfig(AppConfig):
    name = 'user_operations'
    verbose_name = "操作管理"

    # def ready(self):
    #     import user_operations.signals

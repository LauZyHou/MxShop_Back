# 系统的包
from datetime import datetime

# 第三方包
from django.contrib.auth.models import AbstractUser
from django.db import models

# 自己的包
pass


class UserProfile(AbstractUser):
    """用户,由手机号标识"""
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    # 用户注册时用的是mobile,没提供name之类的信息,所以可以为null
    # 注意null针对数据库,blank针对表单
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话", help_text="电话号码")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    # py2里才有string转Unicode,py3里默认都是Unicode,直接用__str__()
    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    """
    短信验证码,由手机号关联,回填验证码进行验证。可以保存在redis中
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

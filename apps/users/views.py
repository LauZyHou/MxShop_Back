from random import choice

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
# 但是当第三方模块根本不知道你的user model在哪里如何导入呢
from django.contrib.auth import get_user_model
# 这个方法会去setting中找AUTH_USER_MODEL
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from MxShop_Back.privacy import YUNPIAN_KEY
from rest_framework.response import Response
from rest_framework import mixins, permissions, authentication
from rest_framework import viewsets, status
from users.models import VerifyCode
from users.serializers import SmsSerializer\
    # , UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则:对用户名和手机号都可以验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    点击发送短信验证码时向此view请求
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """生成验证码,调用云片接口发送,并将验证码保存到数据库"""
        # 验证mobile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 这里验证失败会raise一个ValidationError而不执行后面的
        mobile = serializer.validated_data["mobile"]  # 取出通过验证的mobile
        # 云片网发送短信
        yun_pian = YunPian(YUNPIAN_KEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        # 发送失败
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]  # 这里将云片网发送短信接口的错误信息放到mobile字段了
            }, status=status.HTTP_400_BAD_REQUEST)  # 遵循REST规范,用HTTP状态码表征请求的结果如何
        # 发送成功
        else:
            code_record = VerifyCode(code=code, mobile=mobile)  # 验证码,手机号对应
            code_record.save()  # 保存到数据库
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

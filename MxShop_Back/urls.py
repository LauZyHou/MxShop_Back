"""MxShop_Back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views

# from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
# from rest_framework.routers import DefaultRouter
# from goods.views_base import GoodsListView
from rest_framework.routers import DefaultRouter
import xadmin
from xadmin.plugins import xversion
from rest_framework_jwt.views import obtain_jwt_token

from MxShop_Back.settings import MEDIA_ROOT
from goods.views import GoodsViewSet, CategoryViewSet, HotSearchsViewset
from user_operations.views import UserFavViewset
from users.views import SmsCodeViewset, UserViewset

# model自动注册
xadmin.autodiscover()
xversion.register_models()

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsViewSet, base_name="goods")
# 配置category的url
router.register(r'categories', CategoryViewSet, base_name="categories")
# 热搜词
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")
# 配置codes(验证码)的url
router.register(r'code', SmsCodeViewset, base_name="code")
# 配置users的url
router.register(r'users', UserViewset, base_name="users")
# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

urlpatterns = [
    path('', include(router.urls)),
    path(r'xadmin/', xadmin.site.urls),
    # 富文本相关url
    path(r'ueditor/', include('DUEditor.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 自动化文档,1.11版本中注意此处前往不要加$符号
    path('docs/', include_docs_urls(title='mtianyan超市文档')),
    # DRF调试登录,配置了这个才会有登录按钮
    path('api-auth/', include('rest_framework.urls')),
    # drf自带的token授权登录,获取token需要向该地址post数据(username和password)
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证,现在改用这个而不用上面那个drf自带的了
    path('login/', obtain_jwt_token),
]

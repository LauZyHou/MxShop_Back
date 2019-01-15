# MxShop_Back
学习慕学生鲜项目后端，Django REST framework。
## 项目结构
MxShop：项目的配置目录

apps：存放所有app

extra_apps：存放第三方包,有些修改了源码的放在这里最合适

media：媒体文件

templates：项目的静态文件

db_tools：一些用于数据库初始化等的Python脚本

static和collect_static：存放本地静态文件
## 一些操作
### 映射模型到数据库
清空数据库后执行此操作。
```
makemigrations
migrate
```
### 收集静态资源到本地目录
将收集到collect_static目录。
```
collectstatic
```
### 创建超级用户
```
createsuperuser
```
### 初始化数据库
运行db_tools下的两个脚本。因为外键约束，应先导入类别数据，再导入商品数据。
## 相关资源
### 学习视频
```
https://www.bilibili.com/video/av40066981
```
### XAdmin for Django2
```
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2
```
### DUEitor
这是DjangoUEditor的个人维护版，支持Django2，直接下载使用。
```
https://github.com/dhcn/DUEditor
```
### VueDjangoFrameWorkShop
这是依照该项目教学视频的一个学员的实现，在这里可以找到视频中项目后端源码。
```
https://github.com/mtianyan/VueDjangoFrameWorkShop
```

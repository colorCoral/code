"""admin url
这里主要是后台的功能，咨询师，后台管理者使用
这里主要是后台url的分发
从anima里面的urls分发过来
"""
from django.conf.urls import url
from admin import views

urlpatterns = [

    # 注册 -- 暂时不开放(未开发)
    url(r'^h_register/$', views.register, name='register'),

    # 登录
    url(r'^h_login/$', views.login, name='login'),

    # 后台首页展示
    url(r'^h_index/$', views.h_index, name='h_index'),

    # 咨询师信息展示
    url(r'^h_user/$', views.h_user, name='h_user'),


]

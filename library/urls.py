#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings

import library.views as views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  #登录
                  url(r'^login/', views.user_login, name='user_login'),
                  #登出
                  url(r'^logout/', views.user_logout, name='user_logout'),
                  #注册
                  url(r'^register/', views.user_register, name='user_register'),
                  #修改密码
                  url(r'^set_password/', views.set_password, name='set_password'),
                  #没有serve这个views
                  #url(r'^static/(?P<path>.*)$', static_views.serve, name='static'),
                  #书籍细节
                  url(r'^book/detail$', views.book_detail, name='book_detail'),
                  #读者操作：还书和续借功能
                  url(r'^book/action$', views.reader_operation, name='reader_operation'),
                  #书籍查询
                  url(r'^search/', views.book_search, name='book_search'),
                  #个人信息
                  url(r'^profile/', views.profile, name='profile'),
                  #统计信息
                  url(r'^statistics/', views.statistics, name='statistics'),
                  #关于
                  url(r'^about/', views.about, name='about'),

                  #张丽的自定义url
                  #从导航栏进入检索历史
                  url(r'^showsearchlist/', views.show_mysearchlist, name='showsearchlist'),
                  #添加至检索历史
                  url(r'^searchlist/', views.add_to_searchlist, name='searchlist'),
                  #测试入口
                  url(r'^test/', views.test, name='test'),
                  #删除检索历史
                  url(r'^delete/', views.delete_from_searchlist, name='delete_searchlists'),
                  #个人图书馆界面
                  url(r'^mylib/', views.mylib, name='mylib'),
                  #从个人图书馆中删除书籍
                  url(r'^mylib/delete$', views.delete_from_mylib, name='delete_from_mylib'),
                  #
                  #url(r'^mylib/action$', views.mylib, name='test_mylib'),
                    #个人中心的url群
                  #修改个人信息
                  url(r'^changeinfo/', views.pers_changeinfo, name='changeinfo'),
                  #通知展示列表
                  url(r'^notice/', views.pers_notice, name='notice'),
                  #展示通知内容
                  url(r'^shownotice/detail$', views.show_pers_notice, name='notice_detail'),
                  #我的借阅情况
                  url(r'^bowrrowing/', views.pers_borrowing, name='borrowing_situation'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

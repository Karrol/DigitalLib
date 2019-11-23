#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import uuid, os


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename


class Reader(models.Model):
    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='读者')
    name = models.CharField(max_length=16, unique=True, verbose_name='姓名')
    phone = models.IntegerField(unique=True, verbose_name='电话')
    max_borrowing = models.IntegerField(default=5, verbose_name='可借数量')
    balance = models.FloatField(default=0.0, verbose_name='余额')
    photo = models.ImageField(blank=True, upload_to='media', verbose_name='头像')
    # <---demo数据库字段与我们设计的数据库字段分割线-->
    # readerType = models.CharField('读者类型', max_length=11,choices=(('A', '最大可借数目0'), ('B', '最大可借数目15'), ('C', '最大可借数目30')), default='A')
    # telNumber = models.CharField('电话', max_length=20, blank=True)
    email = models.CharField('邮箱', max_length=30, blank=True, default='null')
    idType = models.CharField('证件类型', max_length=10, choices=(('身份证', 'A'), ('学生证', 'B')), default='A')
    idNumber = models.CharField('证件号码', max_length=20, default='000000000000000000')
    intTime = models.DateField('登记日期', default='2019-11-16')
    readertypeName = models.CharField('读者类型名称', max_length=30, blank=True, default='普通市民')
    # bookNumber = models.IntegerField('书籍上限', max_length=4)
    
    STATUS_CHOICES = (
        (0, 'normal'),
        (-1, 'overdue')
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

    ISBN = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    title = models.CharField(max_length=128, verbose_name='书名')
    author = models.CharField(max_length=32, verbose_name='作者')
    press = models.CharField(max_length=64, verbose_name='出版社')

    description = models.CharField(max_length=1024, default='', verbose_name='详细')
    price = models.CharField(max_length=20, null=True, verbose_name='价格')

    category = models.CharField(max_length=64, default=u'文学', verbose_name='分类')
    cover = models.ImageField(blank=True, upload_to=custom_path, verbose_name='封面',default='null')
    index = models.CharField(max_length=16, null=True, verbose_name='索引')
    location = models.CharField(max_length=64, default=u'图书馆1楼', verbose_name='位置')
    quantity = models.IntegerField(default=1, verbose_name='数量')

    def __str__(self):
        return self.title + self.author


class Borrowing(models.Model):
    class Meta:
        verbose_name = '借阅'
        verbose_name_plural = '借阅'

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='ISBN')
    date_issued = models.DateField(verbose_name='借出时间')
    date_due_to_returned = models.DateField(verbose_name='应还时间')
    date_returned = models.DateField(null=True, verbose_name='还书时间')
    amount_of_fine = models.FloatField(default=0.0, verbose_name='欠款')

    def __str__(self):
        return '{} 借了 {}'.format(self.reader, self.ISBN)

class Mylibrary(models.Model):
    class Meta:
        verbose_name = '我的图书馆'
        verbose_name_plural = '我的图书馆'
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者',default='51')
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='ISBN')
    In_date = models.DateTimeField(verbose_name='加入时间',null=True,blank=True,default=None)

class mysearchlist(models.Model):
    class Meta:
        verbose_name = '我的查询历史'
        verbose_name_plural = '我的查询历史'
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='ISBN')
    search_date = models.DateTimeField(verbose_name='查询时间',null=True,blank=True,default=None)

class  newsColumn_info(models.Model):
    columnName = models.CharField('栏目名', primary_key=True, max_length=20,default='News')
    URL = models.CharField('网址', max_length=200)
    abstract = models.CharField('简介', max_length=200)

class  article_info(models.Model):
    articleID = models.CharField('文章ID', primary_key=True, max_length=20)
    tittle = models.CharField('标题', max_length=200)
    content = models.CharField('正文', max_length=2000)
    pubDate = models.DateTimeField('提交时间')
    author = models.CharField('作者', max_length=200)
    columnName = models.ForeignKey('newsColumn_info', on_delete=models.CASCADE)

class  weekbook(models.Model):
    weekbookID = models.CharField('每周推荐的书籍ID', primary_key=True, max_length=20)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='ISBN')
    articleID = models.ForeignKey(article_info, on_delete=models.CASCADE)
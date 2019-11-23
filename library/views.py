#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.utils import timezone
from django.urls import reverse

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

#from library.models import Book, Reader, User, Borrowing
from .models import *
#from library.models import mysearchlist,Mylibrary,weekbook
from library.forms import SearchForm, LoginForm, RegisterForm, ResetPasswordForm,Change_reader_infoForm



def index(request):
    context = {
        'searchForm': SearchForm(),
    }
    return render(request, 'library/index.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    state = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse(u'Your account is disabled.')
        else:
            state = 'not_exist_or_password_error'

    context = {
        'loginForm': LoginForm(),
        'state': state,
    }

    return render(request, 'library/login.html', context)


def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    registerForm = RegisterForm()

    state = None
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST, request.FILES)
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('re_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            name = request.POST.get('name', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create(username=username)
                new_user.set_password(password)
                new_user.save()
                new_reader = Reader.objects.create(user=new_user, name=name, phone=int(username))
                new_reader.photo = request.FILES['photo']
                new_reader.save()
                state = 'success'

                auth.login(request, new_user)

                context = {
                    'state': state,
                    'registerForm': registerForm,
                }
                return render(request, 'library/register.html', context)

    context = {
        'state': state,
        'registerForm': registerForm,
    }

    return render(request, 'library/register.html', context)


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'

    context = {
        'state': state,
        'resetPasswordForm': ResetPasswordForm(),
    }

    return render(request, 'library/set_password.html', context)


@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


'''def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    borrowing = Borrowing.objects.filter(reader=reader).exclude(date_returned__isnull=False)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'borrowing': borrowing,
    }
    return render(request, 'library/profile.html', context) '''


def reader_operation(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    action = request.GET.get('action', None)

    if action == 'return_book':
        id = request.GET.get('id', None)
        if not id:
            return HttpResponse('no id')
        b = Borrowing.objects.get(pk=id)
        b.date_returned = datetime.date.today()
        if b.date_returned > b.date_due_to_returned:
            b.amount_of_fine = (b.date_returned - b.date_due_to_returned).total_seconds() / 24 / 3600 * 0.1
        b.save()

        r = Reader.objects.get(user=request.user)
        r.max_borrowing += 1
        r.save()

        bk = Book.objects.get(ISBN=b.ISBN_id)
        bk.quantity += 1
        bk.save()

        return HttpResponseRedirect('/bowrrowing?state=return_success')

    elif action == 'renew_book':
        id = request.GET.get('id', None)
        if not id:
            return HttpResponse('no id')
        b = Borrowing.objects.get(pk=id)
        if (b.date_due_to_returned - b.date_issued) < datetime.timedelta(60):
            b.date_due_to_returned += datetime.timedelta(30)
            b.save()

        return HttpResponseRedirect('/bowrrowing?state=renew_success')

    return HttpResponseRedirect('/bowrrowing')


def book_search(request):
    search_by = request.GET.get('search_by', '书名')
    books = []
    current_path = request.get_full_path()

    keyword = request.GET.get('keyword', u'_书目列表')

    if keyword == u'_书目列表':
        books = Book.objects.all()
    else:
        if search_by == u'书名':
            keyword = request.GET.get('keyword', None)
            books = Book.objects.filter(title__contains=keyword).order_by('-title')[0:50]
        elif search_by == u'ISBN':
            keyword = request.GET.get('keyword', None)
            books = Book.objects.filter(ISBN__contains=keyword).order_by('-title')[0:50]
        elif search_by == u'作者':
            keyword = request.GET.get('keyword', None)
            books = Book.objects.filter(author__contains=keyword).order_by('-title')[0:50]
        elif search_by == u'图书目录':
            keyword = request.GET.get('keyword', None)
            books = Book.objects.filter(category__contains=keyword).order_by('-title')[0:50]

    paginator = Paginator(books, 5)
    page = request.GET.get('page', 1)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    # ugly solution for &page=2&page=3&page=4
    if '&page' in current_path:
        current_path = current_path.split('&page')[0]

    context = {
        'books': books,
        'search_by': search_by,
        'keyword': keyword,
        'current_path': current_path,
        'searchForm': SearchForm(),
    }
    return render(request, 'library/search.html', context)


def book_detail(request):
    ISBN = request.GET.get('ISBN', None)
    print(ISBN)
    if not ISBN:
        return HttpResponse('there is no such an ISBN')
    try:
        book = Book.objects.get(pk=ISBN)
    except Book.DoesNotExist:
        return HttpResponse('there is no such an ISBN')

    action = request.GET.get('action', None)
    state = None

    if action == 'borrow':

        if not request.user.is_authenticated:
            state = 'no_user'
        else:
            reader = Reader.objects.get(user_id=request.user.id)
            if reader.max_borrowing > 0:
                reader.max_borrowing -= 1
                reader.save()

                bk = Book.objects.get(pk=ISBN)
                bk.quantity -= 1
                bk.save()

                issued = datetime.date.today()
                due_to_returned = issued + datetime.timedelta(30)

                b = Borrowing.objects.create(
                    reader=reader,
                    ISBN=bk,
                    date_issued=issued,
                    date_due_to_returned=due_to_returned)

                b.save()
                state = 'success'
                #2019/11/19 怎么实现借阅的跳转逻辑值得思考学习profile，目前有bug
                return HttpResponseRedirect('/bowrrowing?state=borrow_success')
            else:
                state = 'upper_limit'

    if action == 'add_to_mylib':

        if not request.user.is_authenticated:
            state = 'no_user'
        else:
            reader = Reader.objects.get(user_id=request.user.id)
            bk = Book.objects.get(pk=ISBN)
            bk.save()
            #不确定数据库中是否有这个记录时要用filter筛选并且进行判断，如果直接使用get方法，数据库中不存在这条记录就会报错
            myliblist = Mylibrary.objects.filter(ISBN=ISBN,reader=reader)
            if myliblist.exists():
                state = 'repeat_add'
                return HttpResponseRedirect('/mylib?state=repeat_add')
            else:
                issued = timezone.now()

                b = Mylibrary.objects.create(
                    reader=reader,
                    ISBN=bk,
                    In_date=issued)

                b.save()
                state = 'add_success'
                return HttpResponseRedirect('/mylib?state=add_success')
    context = {
        'state': state,
        'book': book,
    }
    return render(request, 'library/book_detail.html', context)


def statistics(request):
    borrowing = Borrowing.objects.all()
    readerInfo = {}
    for r in borrowing:
        if r.reader.name not in readerInfo:
            readerInfo[r.reader.name] = 1
        else:
            readerInfo[r.reader.name] += 1

    bookInfo = {}
    for r in borrowing:
        if r.ISBN.title not in bookInfo:
            bookInfo[r.ISBN.title] = 1
        else:
            bookInfo[r.ISBN.title] += 1

    readerData = list(sorted(readerInfo, key=readerInfo.__getitem__, reverse=True))[0:10]
    bookData = list(sorted(bookInfo, key=bookInfo.__getitem__, reverse=True))[0:5]

    readerAmountData = [readerInfo[x] for x in readerData]

    bookAmountData = [bookInfo[x] for x in bookData]

    context = {
        'readerData': readerData,
        'readerAmountData': readerAmountData,
        'bookData': bookData,
        'bookAmountData': bookAmountData,
    }
    return render(request, 'library/statistics.html', context)


def about(request):
    return render(request, 'library/about.html', {})




#张丽的自定义函数



#从检索首页的导航栏入口进入查询结果页
@login_required
def show_mysearchlist(request):
    searchlists = []
    # 获取当前页面的url
    current_path = request.get_full_path()
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        # 获取传递过来读者ID
        reader = Reader.objects.get(user_id=request.user.id)
        searchlists= mysearchlist.objects.filter(reader=reader).order_by('-search_date')[0:50]

        # 翻页功能实现
        paginator = Paginator(searchlists, 5)
        page = request.GET.get('page', 1)

        try:
            searchlists = paginator.page(page)
        except PageNotAnInteger:
            searchlists = paginator.page(1)
        except EmptyPage:
            searchlists = paginator.page(paginator.num_pages)

        # ugly solution for &page=2&page=3&page=4
        if '&page' in current_path:
            current_path = current_path.split('&page')[0]
            
        context = {
            'current_path': current_path,
            
            "searchlists": searchlists,
           
        }
        return render(request, 'library/searchlist.html', context)


#将搜索结果添加至“查询结果”页面
@login_required
# @permission_required('Information.delete_information', raise_exception=True)
def add_to_searchlist(request):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        # 获取传递过来的ISBN号以及读者ID
        variables = request.GET['ISBN']
        reader = Reader.objects.get(user_id=request.user.id)
        #实现数据库添加操作，实现“查询界面”的数据传递到“查询结果”页面
        for item in variables.split(','):  # 拆分多个ISBN号连结而成的字符串，形成ISBN号列表
            #定义一个临时的书籍对象来存储数据信息
            bk = Book.objects.get(ISBN=item)
            # bk.quantity -= 1   #电子书不需要库存减一
            bk.save()
            date = timezone.now()
            #在表“mysearchlist”中创建记录存bk对象的数据
            searchlist = mysearchlist.objects.create(
                reader=reader,
                ISBN=bk,  # 注意：这样赋值后，书的ISBN是个BOOK实例！？以致于在template代码中有Book.ISBN.ISBN的变量出现
                search_date=date)
            searchlist.save()
        state = 'success'#数据库存取操作完成
        if (state == 'success'):
            searchlists = mysearchlist.objects.filter(reader=reader)
            context = {"searchlists": searchlists}
            return render(request, 'library/searchlist.html', context)

    return HttpResponseRedirect(reverse('library:searchlist'))

#删除“查询结果”页面中的书籍
@login_required
# @permission_required('Information.delete_information', raise_exception=True)
def delete_from_searchlist(request):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        # 获取传递过来的查询记录的id以及读者ID
        variables = request.GET['id']
        reader = Reader.objects.get(user_id=request.user.id)
        #实现数据库添加操作，实现“查询界面”的数据传递到“查询结果”页面
        for item in variables.split(','):  # 拆分多个查询记录id连结而成的字符串，形成id列表
            bk = get_object_or_404(mysearchlist, pk=int(item))
            bk.delete()
        state = 'success'#数据库删除操作完成
        if (state == 'success'):
            searchlists = mysearchlist.objects.filter(reader=reader)
            context = {"searchlists": searchlists}
            return render(request, 'library/searchlist.html', context)

    return HttpResponseRedirect(reverse('library:searchlist'))

#test 删除"查询列表的"记录
@login_required
def test(request):
    searchlists = []
    # 获取当前页面的url
    current_path = request.get_full_path()
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        # 获取传递过来读者ID
        reader = Reader.objects.get(user_id=request.user.id)
        searchlists = mysearchlist.objects.filter(reader=reader).order_by('-search_date')[0:50]

        # 翻页功能实现
        paginator = Paginator(searchlists, 5)
        page = request.GET.get('page', 1)

        try:
            searchlists = paginator.page(page)
        except PageNotAnInteger:
            searchlists = paginator.page(1)
        except EmptyPage:
            searchlists = paginator.page(paginator.num_pages)

        # ugly solution for &page=2&page=3&page=4
        if '&page' in current_path:
            current_path = current_path.split('&page')[0]

        context = {
            'current_path': current_path,

            "searchlists": searchlists,

        }
        return render(request, 'library/searchlist.html', context)





#显示“我的图书馆”页面，添加图书到我的图书馆页面的代码见“def book_detail”
#"def mylib"应该完成显示我的图书馆书籍
def mylib(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    mylib_list = Mylibrary.objects.filter(reader=reader)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'mylib_list': mylib_list,
    }
    return render(request, 'library/mylib.html', context)

#提供删除我的图书馆内书籍的功能-未开发完毕，还需学习借书、还书实现的过程
def delete_from_mylib(request):
    isbn = request.GET.get('ISBN', None)
    print(isbn)
    '''if not ISBN:
        return HttpResponse('there is no such an ISBN')
    try:
        book = Book.objects.get(pk=ISBN)
    except Book.DoesNotExist:
        return HttpResponse('there is no such an ISBN')'''

    action = request.GET.get('action', None)
    state = None
    
    #获取用户信息
    id = request.user.id
    reader = Reader.objects.get(user_id=id)
    if action=='delete_from_mylib':
        book=Mylibrary.objects.get(reader=reader,ISBN=isbn)
        book.delete()
        book.save()
        state='delete_from_mylib_success'
        return HttpResponseRedirect('/mylib?state=delete_from_mylib_success')
    else:
        state='delete_from_mylib_fail'
        return HttpResponseRedirect('/mylib?state=delete_from_mylib_fail')
        
    '''mylib_list= Mylibrary.objects.filter(reader=reader)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'mylib_list': mylib_list,
    }
    return render(request, 'library/mylib.html', context)'''
    
#个人中心页面-个人资料
def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    borrowing = Borrowing.objects.filter(reader=reader).exclude(date_returned__isnull=False)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'borrowing': borrowing,
    }
    return render(request, 'library/pers_profile.html', context)

#读者修改个人信息表单
@login_required
def pers_changeinfo(request):
    reader = Reader.objects.get(user=request.user)
    state = None
    if request.method == 'POST':
        reader.name = request.POST.get('name', '')
        # photo的上传有问题，还有就是要给读者原始信息的提示
        reader.photo = request.POST.get('photo', '')
        reader.email = request.POST.get('email', '')
        reader.idType = request.POST.get('idType', '')
        reader.idNumber = request.POST.get('idNumber', '')
        reader.save()
        state = 'success'
    context = {
        'Change_reader_infoForm': Change_reader_infoForm(),
        'state': state,
    }

    return render(request, 'library/pers_changeinfo.html', context)

        

#个人中心-读者通知界面 
@login_required
def pers_notice(request):
    reader = Reader.objects.get(user=request.user)
    notice_week = article_info.objects.filter(columnName='每周一书')
    notice_lend = article_info.objects.filter(columnName='借阅催还')
    nowtime = timezone.now()

    context={
        "reader":reader,
        #"state":state,
        "notice_week":notice_week,
        "notice_lend":notice_lend,
        "nowtime":nowtime,

    }
    return  render(request,'library/pers_notice.html', context)

#个人中心-读者通知阅读界面  （11/19工作，将通知界面和借阅界面写好）
@login_required
def show_pers_notice(request):
    articleID = request.GET.get('aticleID', None)
    print(articleID)
    if not articleID:
        return HttpResponse('there is no such an aticleID')
    try:
        notice = article_info.objects.get(pk=articleID)
    except notice.DoesNotExist:
        return HttpResponse('there is no such an articleID')
    state=None
    #如果是每周一书，则要显示书籍的信息
    #之前使用colum名称“每周一书”判断
    if notice.articleID.startswith('week'):
        #获取书籍的信息
        wbook=weekbook.objects.get(articleID=articleID)
        wbook_info=Book.objects.get(pk=wbook.ISBN.ISBN)
        state='weekbook_notice'
       # wbook.ISBN=wbook_info
        #wbook.save()
        context = {
            'wbook_info': wbook_info,
            'notice': notice,
            'state':state,
        }
        return render(request, 'library/notice_detail.html', context)
    else:
        state='normal_notice'
        context={'notice': notice,
                 'state':state,}
        return render(request, 'library/notice_detail.html', context)
    


#查询借阅状态页面
def pers_borrowing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    borrowing = Borrowing.objects.filter(reader=reader).exclude(date_returned__isnull=False)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'borrowing': borrowing,
    }
    return render(request, 'library/pers_borrow_situation.html', context)


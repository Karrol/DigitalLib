#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label=u'用户名：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        label=u'密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
        }),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=u'用户名/手机号码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        }),
    )
    name = forms.CharField(
        label=u'名字：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'name',
            'id': 'id_name',
        }),
    )
    password = forms.CharField(
        label=u'密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'id_password',
        }),
    )
    re_password = forms.CharField(
        label=u'重复密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 're_password',
            'id': 'id_re_password',
        }),
    )
    email = forms.CharField(
        label=u'电子邮件：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'id': 'id_email',
        }),
        required=False,
    )

    photo = forms.FileField(
        label=u'头像：',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'name': 'photo',
            'id': 'id_photo',
        }),
        required=False,
    )

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        label=u'原始密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'old_password',
            'id': 'id_old',
        }),
    )
    new_password = forms.CharField(
        label=u'新密码：',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'new_password',
            'id': 'id_new',
        }),
    )
    repeat_password = forms.CharField(
        label=u'重复密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'repeat_password',
            'id': 'id_repeat',
        }),
    )

class SearchForm(forms.Form):
        CHOICES = [
            (u'ISBN', u'ISBN'),
            (u'书名', u'书名'),
            (u'作者', u'作者'),
            (u'图书目录', u'图书目录')
        ]

        search_by = forms.ChoiceField(
            label='',
            choices=CHOICES,
            widget=forms.RadioSelect(),
            initial=u'书名',
        )

        keyword = forms.CharField(
            label='',
            max_length=32,
            widget=forms.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': u'请输入需要检索的图书信息',
                'name': 'keyword',
            })
        )

#张丽的自定义表单

#读者更改个人信息的表单-模型表单
class Change_reader_infoForm(forms.ModelForm):
    #步骤1：添加模型外的表单字段
    #此处无

    #步骤2：模型与表单设置
    class Meta:
        #绑定模型，必选
        model = Reader
        #设置转换字段，必选，属性值为'__all__'时全部转换
        #fields = '__all__'
        fields = ['name','photo','email','idType','idNumber']
        #禁止模型转换的字段，可选，若设置了该属性，fields则可以不设置
        exclude = ['user','phone','max_borrowing','balance','status','intTime','readertypeName']
        #设置HTML元素控件的label标签，可选
        labels = {'name':'姓名',
                  'email':'邮箱',
                  'idType':'证件类型',
                  'idNumber':'证件号码',
                  'photo': '头像',
            }
        #定义字段的类型，可选，默认时自动转换的
        field_classes = {
            'name': forms.CharField,
            }
        #设置提示信息
        help_texts = {
            'name':'',
            }
        #自定义错误信息
        error_messages = {
            #设置全部错误信息
            '__all__':{'required':'请输入内容',
                       'invalid':'请检查输入内容'},
            #设置某个字段的错误信息
            'weight':{'required':'请输入重量数值',
                      'invalid':'请检查数值是否正确'},
            }

    #步骤3： 自定义表单字段的数据清洗
    def clean_weight(self):
        #获取字段weight的值
        idnumber = self.cleaned_data['idNumber']
        return idnumber
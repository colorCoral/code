import re
from django import forms
from django.forms import widgets
from project import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class UserForm(forms.Form):

    username = forms.CharField(max_length=16, min_length=1, label='用户名',
                               error_messages={
                                'required': '这个字段必须填写',
                                'max_length': '最大不能超过32位',
                                'min_length': '最小不能超过1位'

                               },)
    password = forms.CharField(max_length=16, min_length=6, label="密码",
                               error_messages={
                                   'required': '这个字段必须填写',
                                   'max_length': '最大不能超过32位',
                                   'min_length': '最小不能低于6位'
                               },
                               widget=widgets.PasswordInput
                               )

    r_password = forms.CharField(max_length=16, min_length=6, label="重复密码",
                                 error_messages={
                                   'required': '这个字段必须填写',
                                   'max_length': '最大不能超过32位',
                                   'min_length': '最小不能低于6位'
                                 },
                                 widget=widgets.PasswordInput)

    email = forms.EmailField(max_length='32', min_length='5', label='邮箱',
                             error_messages={
                                 'required': '这个字段必须填写',
                                 'max_length': '最大不能超过32位',
                                 'min_length': '最小不能超过5位'
                             })

    def clean_username(self):
        """验证用户名"""
        val = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        user_obj = models.UserInfo.objects.filter(Q(username=val) | Q(email=email))

        if user_obj:
            raise ValidationError('该用户或邮箱以及存在，请重新换一个')
        else:
            return val

    def clean_password(self):
        """验证密码"""
        val = self.cleaned_data.get('password')
        if val.isdecimal():
            raise ValidationError("密码不能为纯数字")
        else:
            return val

    def clean_email(self):
        """验证邮箱"""
        val = self.cleaned_data.get('email')
        if re.search(r'\w+@qq.com$', val):
            return val
        else:
            raise ValidationError("必须是qq邮箱")

    def clean(self):
        """全局钩子，用于比较多个值的时候使用"""
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')

        if password != r_password:
            raise ValidationError("密码必须相同")
        else:
            return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',

            })


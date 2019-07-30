import re
from django import forms
from django.forms import widgets
from project import models

from django.core.exceptions import ValidationError


class UserForm(forms.Form):

    username = forms.CharField(max_length=15, min_length=2,
                               error_messages={
                                   'required': '这个字段必须填写',
                                   'max_length': '最大不能超过15位',
                                   'min_length': '最小不能低于3位'
                               },)

    password = forms.CharField(max_length=32, min_length=6,
                               error_messages={
                                   'required': '这个字段必须填写',
                                   'max_length': '最大不能超过15位',
                                   'min_length': '最小不能低于3位'
                               },
                               widget=widgets.PasswordInput
                               )

    r_password = forms.CharField(max_length=32, min_length=3, label='重复密码',
                                 error_messages={
                                     'required': '这个字段必须填写!',
                                     'max_length': '最大不能超过32位',
                                     'min_length': '最小不能低于3位'},
                                 widget=widgets.PasswordInput
                                 )

    email = forms.EmailField(max_length=32, label='邮箱',
                             error_messages={
                                'required': '这个字段必须填写',
                                'max_length': '最大不能超过32位',
                                'invalid': '邮箱格式不对'
                             }
                             )

    def clean_name(self):
        val = self.cleaned_data.get('username')
        user_obj = models.UserInfo.objects.filter(username=val).first

        if user_obj:
            raise ValidationError('该用户名已存在')
        else:
            return val

    def clean_password(self):
        val = self.cleaned_data.get('password')
        # isdecimal 比 isdigit更能判断数字
        if val.isdecimal():
            raise ValidationError('密码不能为纯数字')
        else:
            return val

    def clean_email(self):
        val = self.cleaned_data.get('email')
        if re.search('\w+@163.com$', val):
            return val
        else:
            raise ValidationError('必须是163邮箱')

    # 全局钩子,用于比较两个值
    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')

        if password != r_password:
            self.add_error('r_password', '两次密码不一致')
        else:
            return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

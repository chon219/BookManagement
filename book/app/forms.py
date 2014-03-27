# -*- coding: utf-8 -*-
# Chon<chon219@gmail.com>

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User

class BookAddForm(forms.Form):
    title = forms.CharField(max_length=256)
    title.widget.attrs['class'] = 'form-control'
    author = forms.CharField(max_length=256)
    author.widget.attrs['class'] = 'form-control'
    press = forms.CharField(max_length=256)
    press.widget.attrs['class'] = 'form-control'
    year = forms.CharField(max_length=16)
    year.widget.attrs['class'] = 'form-control'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    username.widget.attrs['class'] = 'form-control'
    password = forms.CharField(max_length=60, widget=forms.PasswordInput, required=True)
    password.widget.attrs['class'] = 'form-control'
    def clean(self):
        if "username" not in self.cleaned_data:
            self._errors['username'] = ErrorList([u'请输入用户名'])
            return self.cleaned_data
        if "password" not in self.cleaned_data:
            self._errors['password'] = ErrorList([u'请输入密码'])
            return self.cleaned_data
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                self._errors['username'] = ErrorList([u'此用户已被禁用'])
            if not user.check_password(password):
                self._errors['password'] = ErrorList([u'密码错误'])
        except User.DoesNotExist:
            self._errors['username'] = ErrorList([u'此用户不存在'])
        return self.cleaned_data

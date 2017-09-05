#!/bin/env python
# coding:utf8

from django import forms


class AccountForm(forms.Form):
    account = forms.CharField(label='域帐号', max_length=15)

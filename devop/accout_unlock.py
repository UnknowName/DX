#!/bin/env python
# coding:utf8


from django.shortcuts import HttpResponse, render
from django.conf import settings

from .forms import AccountForm
from .cls import LDAP



def index(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data.get('account', None)
            ldap = LDAP()
            user = ldap.get_dn(account)
            if user:
                return HttpResponse(u'已成功解琐帐号%s<a href="/ldap/">返回</a>' %(account,))
            else:
                return HttpResponse(u'没有找到用户%s,请确认输入正确' %(account,))
    else:
        form = AccountForm()
    return render(request, 'unlock.html', locals())

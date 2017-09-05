#!/bin/env python
# coding:utf8


from django.shortcuts import HttpResponse, render
from django.conf import settings

from .forms import AccountForm
from .cls import LDAP
import logging

logger = logging.getLogger('django')


def index(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data.get('account', None)
            ldap = LDAP()
            dn = ldap.get_dn(account)
            logger.info(dn)
            ldap.unlock(dn)
            if ldap.is_right():
                logger.info('Unlcok user %s successful' % (account,))
                return HttpResponse(u'已成功解琐帐号%s<a href="/ldap/">返回</a>' %(account,))
            else:
                return HttpResponse(u'解琐失败，请确认用户名正确或者联系管理员')
    else:
        form = AccountForm()
    return render(request, 'unlock.html', locals())

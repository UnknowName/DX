#!/bin/env python
# coding:utf8


from django.conf import settings
from django.shortcuts import HttpResponse, render

import logging
from .forms import FileForm

logger = logging.getLogger('django')


def index(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            filename = request.FILES['filename']
            print type(filename)
            pass
    else:
        form = FileForm()
    return render(request, 'cache.html', locals())

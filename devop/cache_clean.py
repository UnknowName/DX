#!/bin/env python
# coding:utf8


from django.conf import settings
from django.shortcuts import HttpResponse, render

import json
import logging
import requests
from tld import get_tld

from .forms import FileForm

logger = logging.getLogger('django')


def index(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            up_file = request.FILES['filename']
            if not up_file.name.endswith('.txt'):
                return HttpResponse(u'抱歉，仅支持文本格式文件')
            clean_dic = dict()
            for url in up_file:
                if url.strip():
                    try:
                        domain = get_tld(url)
                    except Exception:
                        return HttpResponse(u'待清理的缓存URL不合法，请检查')
                    clean_dic.setdefault(domain, list()) 
                    clean_dic[domain].append(url)
            api_resp = requests.get(
                settings.CLOUDFLARE_API,
                headers=settings.CLOUDFLARE_HEADER
            ).json()
            zone_dic = dict()
            for dic in api_resp['result']:
                zone_dic[dic['name']] = dic['id']
            for domain,urls in clean_dic.items():
                data = {
                    "files": urls,
                    "tags": [ "some-tag", "another-tag"]
                }
                del_api_fmt = '%s/%s/purge_cache'
                resp = requests.delete(
                    del_api_fmt % (settings.CLOUDFLARE_API, zone_dic[domain]),
                    headers=settings.CLOUDFLARE_HEADER,
                    data=json.dumps(data)
                ).json()
                if not resp['success']:
                    logger.error(resp)
                    return HttpResponse(u'清理缓存失败,请重试或联系管理员')
            return HttpResponse(u'清理缓存成功')
    else:
        form = FileForm()
    return render(request, 'cache.html', locals())

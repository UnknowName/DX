#!/bin/env python
# coding:utf8


from django.shortcuts import HttpResponse, render

import json
import re
from devop.models import DXSystemInfo
from devop.funcs import create_fqdn, fmt_host, get_site_app
from devop.ldap_auth import LDAPAuth


def index(request):
    return render(request, 'index.html')


def query(request, sys_name, data_format=None, sys_type=None):
    system_type = 'PUB' if sys_type.upper() == 'W' else 'API'
    system_type = 'WIN' if sys_type.upper() == 'P' else system_type
    sys_obj = DXSystemInfo.objects.filter(
        system_name=sys_name
    ).filter(
        system_type=system_type
    )
    err_info = {
        'sys_name': sys_name.lower(),
        'status': 404,
        'debug_info': 'Not Found!'
    }
    if not sys_obj:
        return HttpResponse(json.dumps(err_info))
    server_info = dict()
    server_info['status'] = 200
    server_info['infos'] = []
    server_info['system_name'] = sys_name.lower()
    for info in sys_obj:
        sys_info = dict()
        if system_type != 'WIN':
            sys_info['url'] = info.use_domain
            sys_info['website'] = info.system_server_name
            sys_info['nginx'] = create_fqdn(info.system_ngx_server)
        else:
            sys_info['path'] = info.use_domain
            sys_info['process_name'] = info.system_server_name
        sys_info['iis'] = create_fqdn(info.system_iis_server)
        server_info['infos'].append(sys_info)
    if data_format == 'json' or not data_format:
        return HttpResponse(json.dumps(server_info))
    elif data_format == 'str':
        url = sys_info['url']
        host = sys_info['iis']
        site_url = re.split(r'[http//:|https//:]//', url)[-1]
        if '/' in site_url:
            site, app = site_url.split('/', 1)
        else:
            site = site_url
        if not isinstance(host, list):
            return render(request, 'hosts.yaml', locals())
        else:
            host = ':'.join(host)
            return render(request, 'hosts.yaml', locals())


def generate_yaml(request, sys_name, sys_type):
    server_name = request.META['QUERY_STRING']
    system_type = 'PUB' if sys_type.upper() == 'W' else 'API'
    system_type = 'WIN' if sys_type.upper() == 'P' else system_type
    try:
        sys_obj = DXSystemInfo.objects.get(
            system_name=sys_name, system_type=system_type,
            system_server_name=server_name
        )
    except Exception:
        return HttpResponse(404)
    fqdn_host = create_fqdn(sys_obj.system_iis_server)
    host = fmt_host(fqdn_host)
    nginx = create_fqdn(sys_obj.system_ngx_server)
    if not isinstance(nginx, list):
        nginxs = []
        nginxs.append(nginx)
    else:
        nginxs = nginx
    app = sys_obj.system_server_name
    if sys_obj.use_domain:
        site = get_site_app(sys_obj.use_domain)[0]
    return render(request, 'hosts.yaml', locals())


def get_all(request):
    apis = DXSystemInfo.objects.filter(system_type='API')
    return render(request, 'all.yaml', locals())

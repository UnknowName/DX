#!/bin/env python
# coding:utf8


import re
import json
import requests
from tld import get_tld

from django.conf import settings

settings.configure()

print dir(settings)


def create_fqdn(name):
    names = re.split(r'[/,,,\s]', name.lower())
    if not name:
        return ''
    fqdn_names = []
    for name in names:
        name = 'dal05' + name if not name.startswith(('dal05', 'sz')) else name
        if name.startswith('sz') and not name.endswith('corp.dx'):
            name = name + '.corp.dx'
        else:
            name = name + '.sl.dx' if not name.endswith(('sl.dx', 'corp.dx')) else name
        fqdn_names.append(name)
    if len(fqdn_names) == 1:
        return fqdn_names[0]
    else:
        return fqdn_names


def get_site_app(url):
    url = re.split(r'[http//:|https//:]//', url)[-1]
    if '/' in url:
        site,app = url.split('/',1)
        return  site,app
    else:
        return  url


def fmt_host(host):
    if isinstance(host,list):
        return ':'.join(host)
    else:
        return host

def get_zones():
    pass

if __name__ == "__main__":
    print create_fqdn('gw8,gw9')
    print create_fqdn('gw8')
    print create_fqdn('')
    get_zones()

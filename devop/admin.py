#!/bin/env python
# coding:utf8


from django.contrib import admin
from devop.models import DXSystemInfo
from devop.models import PortalInfo


class DXSystemInfoAdmin(admin.ModelAdmin):
    search_fields = ('system_name', 'system_iis_server', 'system_ngx_server')
    list_display = ('system_type', 'system_name', 'system_server_name', 
        'system_iis_server', 'use_domain'
    )


class PortalInfoAdmin(admin.ModelAdmin):
    search_fields = ('dev_user', 'dev_pass', 'portal_user', 'portal_pass')
    list_display = ('dev_user', 'dev_pass', 'portal_user', 'portal_pass')


admin.site.register(DXSystemInfo, DXSystemInfoAdmin)
admin.site.register(PortalInfo, PortalInfoAdmin)

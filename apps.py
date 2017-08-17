#!/bin/env python
# coding:utf8


from django.apps import AppConfig


class DevopConfig(AppConfig):
    name = 'devop'
    verbose_name = u'CMDB系统'


class AuthConfig(AppConfig):
    name = 'django.contrib.auth'
    verbose_name = u'用户系统'

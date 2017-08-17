#!/bin/env python
# coding:utf8


from django.db import models


class DXDeploy(models.Model):
    sites = (
        ('M', 'm.dx.com'),
        ('W', 'www.dx.com'),
    )
    envs = (
        ('T', 'Test OFFline'),
        ('P', 'Product Online')
    )
    site_type = models.CharField(
        max_length=20, choices=sites, verbose_name=u'站点类型'
    ) 
    site_env = models.CharField(
        max_length=20, choices=envs, default='T', verbose_name =u'应用环境'
    )
    app_name = models.CharField(
        max_length=100, blank=True, verbose_name=u'应用名称') 
    app_config_file = models.CharField(
        max_length=100, blank=True, verbose_name=u'配置文件路径')
    app_config_key = models.CharField(
        max_length=100, blank=True, verbose_name=u'配置项键名')
    app_config_value = models.CharField(
        max_length=500, blank=True, verbose_name=u'配置项键值')

    
    class Meta:
        verbose_name = u'配置信息'
        verbose_name_plural = u'发布配置信息'


    def __unicode__(self):
        return '{site}, {app}, {key}, {value}'.format(
	        site=self.site_type, app=self.app_name,
            key=self.app_config_key, value=self.app_config_value
        )


class DXSystemInfo(models.Model):
    system_types = (
        ('API', 'HTTP/HTTPS API'),
        ('WIN', 'Windows Process'),
        ('PUB', 'Website Service'),
    )
    system_name = models.CharField(max_length=50, verbose_name=u'系统名称')
    system_type = models.CharField(
        max_length=20, choices=system_types, verbose_name=u'服务类型'
    )
    system_server_name = models.CharField(
        max_length=100, blank=True, verbose_name=u'服务名称')
    use_domain = models.CharField(
        max_length=500, blank=True, verbose_name=u'服务入口')
    system_desc = models.TextField(
        max_length=500, blank=True, verbose_name=u'服务描述')
    system_iis_server = models.CharField(
        max_length=100, blank=True, verbose_name=u'后端服务器')
    system_ngx_server = models.CharField(
        max_length=100, blank=True, verbose_name=u'代理服务器')
    system_ngx_conf_path = models.CharField(
        max_length=100, blank=True, verbose_name=u'代理配置文件')
    system_called = models.CharField(
        max_length=100, blank=True, verbose_name=u'服务调用者')
    system_db = models.CharField(
        max_length=400, blank=True, verbose_name=u'服务数据库')
    system_remark = models.TextField(
        max_length=500, blank=True, verbose_name=u'服务备注')


    class Meta:
        verbose_name = u'业务信息'
        verbose_name_plural = u'DX业务信息'


    def __unicode__(self):
        return u'系统名称:%s    服务名称:%s     IIS服务器:%s' % (
            self.system_name, self.system_server_name, self.system_iis_server
        )


class PortalInfo(models.Model):
    dev_user = models.CharField(max_length=100, verbose_name=u'开发调用帐号')
    dev_pass = models.CharField(max_length=100, verbose_name=u'开发调用密码')
    portal_user = models.CharField(max_length=100, verbose_name=u'Portal帐号')
    portal_pass = models.CharField(max_length=100, verbose_name=u'Portal密码')

    class Meta:
        verbose_name = u'Protal帐号'
        verbose_name_plural = u'Protal帐号信息'

    def __unicode__(self):
        return '%s %s' % (self.dev_user, self.portal_user)

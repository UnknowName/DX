#!/bin/env python
# coding:utf8

import ldap
import ldap.modlist as modlist
from django.conf import settings
import logging


logger = logging.getLogger('django')


class LDAP(object):
    def __init__(self):
        try:
            self.ldap = ldap.initialize(settings.LDAP_URI)
            self.ldap.bind_s(settings.LDAP_BIND, settings.LDAP_BIND_PASSWD)
        except Exception as e:
            self.e = e
            logger.error(e)

    def get_dn(self, account):
        filter_user = settings.LDAP_FILTER  % (str(account),)
        try:
            result = self.ldap.search_s(
                settings.LDAP_SEARCH, ldap.SCOPE_SUBTREE,
                filter_user, settings.LDAP_DISPLAY_ATTR
            )
        except ldap.FILTER_ERROR:
            return None
        if not result:
            return None
        _, attr_dic = result[0]
        ldap_dn = attr_dic['distinguishedName'][0]
        ldap_user = attr_dic['sAMAccountName'][0]
        if ldap_user == account:
            return ldap_dn

    def is_right(self):
        if not hasattr(self, 'e'):
            return True

    def unlock(self, dn):
        lock_attr = {'lockoutTime': '1'}
        unlock_attr = {'lockoutTime': '0'}
        ldif = modlist.modifyModlist(lock_attr, unlock_attr)
        try:
            self.ldap.modify_s(dn, ldif)
        except Exception as e:
            self.e = e
            logger.error(e)

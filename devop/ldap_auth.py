#!/bin/env python
# coding:utf8


from django.conf import settings
from django.contrib.auth.models import User

import ldap
import logging

logger = logging.getLogger('django')
logger.info('Start LDAP AUTH')

class LDAPAuth(object):
    def __init__(self):
        try:
            self.ldap = ldap.initialize(settings.LDAP_URI)
            self.ldap.bind_s(settings.LDAP_BIND, settings.LDAP_BIND_PASSWD) 
        except Exception as e:
            self.e = e

    def authenticate(self, username=None, password=None, **kwargs):
        if hasattr(self, 'e'):
            raise "Wrong,Because %s" % (self.e,)
        filter_user = settings.LDAP_FILTER  % (username,)
        result = self.ldap.search_s(
            settings.LDAP_SEARCH, ldap.SCOPE_SUBTREE,
            filter_user, settings.LDAP_DISPLAY_ATTR
        )
#       The user not in LDAP,Return None
        if not result:
            return None
        _, attr_dic = result[0]
        ldap_user = attr_dic['sAMAccountName'][0]
        ldap_dn = attr_dic['distinguishedName'][0]
#       The user in LDAP,Authenticat the LDAP password          
        try:
            self.ldap.bind_s(ldap_dn, password)
#            print 'Use The LDAP User %s Login System' % (username,)
        except ldap.INVALID_CREDENTIALS:
            print 'print info'
            logger.error('The LDAP User Or Password Wrong!')
            return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                logger.info('The LDAP User %s not in Django DB,Now Add' % (ldap_user,))
                user = User(
                    username=ldap_user, is_staff=True, 
                    is_superuser=True, is_active=True
                )
                user.set_password(password)
                user.save()
            print 'Return the user object %s' % (user,)
            return user

    def has_perm(self, perm, obj=None):
        return True

    def is_authenticated(self):
        return True
        

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


if __name__ == '__main__':
    print settings.LDAP_URI
    l = LDAPAuth()

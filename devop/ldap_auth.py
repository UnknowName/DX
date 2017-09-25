#!/bin/env python
# coding:utf8


from django.conf import settings
from django.contrib.auth.models import User, Group

import ldap
import logging

logger = logging.getLogger('django')
logger.info('Use LDAPAuth backend')

class LDAPAuth(object):
    def __init__(self):
        try:
            self.ldap = ldap.initialize(settings.LDAP_URI)
            self.ldap.bind_s(settings.LDAP_BIND, settings.LDAP_BIND_PASSWD) 
        except Exception as e:
            logger.error('LDAP bind failed Because %s' % (e,))
            self.e = e

    def authenticate(self, username=None, password=None, **kwargs):
        logger.info('Start the LDAP Auth')
        if hasattr(self, 'e'):
            raise ldap.INVALID_CREDENTIALS
        filter_user = settings.LDAP_FILTER  % (username,)
        result = self.ldap.search_s(
            settings.LDAP_SEARCH, ldap.SCOPE_SUBTREE,
            filter_user, settings.LDAP_DISPLAY_ATTR
        )
#       The user not in LDAP,Return None
        if not result:
            logger.info('The user %s not in LDAP' % (username, ))
            return None
        _, attr_dic = result[0]
        ldap_user = attr_dic['sAMAccountName'][0]
        ldap_dn = attr_dic['distinguishedName'][0]
#       The user in LDAP,Authenticat the LDAP password          
        try:
            self.ldap.bind_s(ldap_dn, password)
            logger.info('The user %s use LDAPAuth sucess' % (username,))
        except ldap.INVALID_CREDENTIALS:
            logger.error('The LDAP User Or Password Wrong!')
            return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                logger.info('The LDAP User %s not in Django DB,Now Add' % (ldap_user,))
                user = User(
                    username=ldap_user, is_staff=True, is_active=True
                )
                dev = Group.objects.get(name='dev')
                user.set_password(password)
                user.save()
                user.groups = [dev]
            return user


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

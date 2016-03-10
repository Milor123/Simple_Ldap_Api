# /usr/bin/env python 2.7
# -*- coding: utf-8 -*-
"""
Title: Simple Ldap Api 1.0
Author: Mateo Bohorquez
Nickname:
 __  __   _   _                  _   ____    _____
|  \/  | (_) | |   ___    _ __  / | |___ \  |___ /
| |\/| | | | | |  / _ \  | '__| | |   __) |   |_ \
| |  | | | | | | | (_) | | |    | |  / __/   ___) |
|_|  |_| |_| |_|  \___/  |_|    |_| |_____| |____/
"""

import ldap
import ldap.modlist as modlist

from functions.convert import *
from functions.show_this import *
from functions.search_this import *
from functions.decorators import *


class Myldap(object):

    @requiere(str, str, str)
    def __init__(self, ip, dn, __password, port='389'):
        # the Distinguished Names (dn) must contain a user and his route, it should have read permission,
        # however read and write should be the best option,
        # because as opposed to read only cant add user or read another directories
        self.ip = ip
        self.dn = dn
        self.__password = __password
        self.port = port
        self.domain = to_domain(dn)
        self.attrib_toshow = []
        self.__connect()

    def __connect(self):
        try:
            self.conn=ldap.initialize("ldap://"+self.ip+":"+self.port)
            self.conn.simple_bind(self.dn, self.__password)  # simple bind changed
            print self.conn.whoami_s()
        except:
            print('Error al conectar a ldap')

    def ldapsearch(self, attrib_forsearch, attrib_toshow, **kwargs):
        self.attrib_toshow = attrib_toshow
        try:
            self.conn.protocol_version = ldap.VERSION3
            self.conn.set_option(ldap.OPT_REFERRALS,0)

            # the code that shown below is waiting for domain or dn such as
            # domain='www.ITFIP.LOCAL', or domain="dc='ITFIP',dc='LOCAL'"
            # added to that, if domain isn't specified, then take default converted domain in the constructor
            # with the to_domain() function
            if 'domain' in kwargs:
                if is_domain_dn(kwargs['domain']):  # verify if is a valid domain
                    self.domain = kwargs['domain']
                elif is_domain_url(kwargs['domain']):
                    self.domain = to_distinguished_name(kwargs['domain'])  # convert url domain to dn
                else:
                    raise NameError('Has escrito un dominio invalido, asegurate de no tener espacios,'
                                    ' por ejemplo dc=ejemplo,dc=com')

            result = self.conn.search_s(self.domain,
                                        ldap.SCOPE_SUBTREE,
                                        attrib_forsearch)

            self.resultssearch = [entry for dn,entry in result if isinstance(entry, dict)]
            if not self.resultssearch:  # if is empty return 0 because not found the search...
                # similar that, "if results == []"
                self.resultssearch = 0
            else:
                self.resultssearch = self.resultssearch[0]
                return self.getsearch()
            # return results[0]
        finally:
            pass
            # self.conn.unbind(), this here can close the connection of ldap

    def ldapadd(self, domain=''):
        #  prototype working :3

        attrs = {}
        attrs['objectclass'] = ['top','organizationalRole','simpleSecurityObject']
        attrs['cn'] = 'replica'
        attrs['userPassword'] = 'aDifferentSecret'
        attrs['description'] = 'User object for replication using slurpd'

        ldif = modlist.addModlist(attrs)
        print attrs
        self.conn.add_s('cn=replica, cn=Users, dc=owner,dc=local', ldif)
        #self.conn.unbind()

    def getsearch(self):

        if self.resultssearch != 0:
            foundit = []
            # first of all take dict keys, which will be compared with attributes specified in (attributetosearch),
            # then add it to new list till loop end
            for key, data in self.resultssearch.iteritems():
                for atrib in self.attrib_toshow:
                    if key.lower() == atrib.lower():  # convert to lower for insensitive case
                        foundit.append([key, data])
            print foundit
            return foundit
        else:
            return 'Lo sentimos lo que has buscado no ha sido encontrado'

    def show(self):
        print self


Nop = Myldap('192.168.0.23', 'cn=administradortest,cn=Users,dc=owner,dc=local','123456789Xx')
Nop.ldapsearch(search_by_mail('a@a.a'), show_name())



#Nop.ldapadd()
#Nop = myldap('192.168.10.28', 'cn=Administrador,cn=Users,dc=ITFIPSALAS,dc=LOCAL', 'Itfip2015')
#print('fin')
#consulta = Nop.ldapsearch(search_by_name('admin'),domain='WWW.ITFIPSALAS.LOCAL')
#print Nop.getsearch(consulta,show_mail())


#Nop.ldapadd()

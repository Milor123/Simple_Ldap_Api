# /usr/bin/env python 2.7
# -*- coding: utf-8 -*-
import ldap
import ldap.modlist as modlist
from functions.convert import *
from functions.show_this import *
from functions.search_this import *
from functions.decorators import *


class Myldap(object):
    """
    firts fo all, this module is specially created for active directory working of the university
    "Instituto Tolimence de Educacion Superior" (ITFIP), where our objective is to ease
    centralization of data through ldap protocol.

    This module establishes a connection to active directory, of Windows Server, by means of a user of domain,
    on top of that, allow data query, and other functions such as, add and modify data, but are still experimentals.

    Attributes:
        conn (instance): instanced connection of ldap object.
        domain (str): DN converted to domain with helpful method.
    """

    def __init__(self, ip, dn, _password, port='389'):
        """
        In the constructor define the sensitive data for Active Directory connection, then call to _connect().

        Args:
            ip (str): ip address.
            dn (str): Distinguished Name.
            _password (str): User password.
            port (str): connection port.

        Attributes:
            ip (str): ip address of domain server.
            dn (str): is a sequence of relative distinguished names (RDN) connected by commas, thus must contain
                administrator user locate and Domain.
            _password (str): you must be specify a adminstrator user of Domain in the Active Directory.
            port (str): Active Directory Domain Services Port.

        .. seealso::
            https://msdn.microsoft.com/en-us/library/windows/desktop/aa366101%28v=vs.85%29.aspx
            https://technet.microsoft.com/en-us/library/dd772723%28v=ws.10%29.aspx

        Example:
            if the connection is valid this should print your user and domain.

            >>> Myldap('192.168.0.23', 'cn=administradortest,cn=Users,dc=owner,dc=local','mypassword')
            u:OWNER\administradortest

        """
        self.ip = ip
        self.dn = dn
        self._password = _password
        self.port = port
        self.domain = to_domain(dn)
        self.conn = object
        self._connect()

    def _connect(self):
        """
        This method will create a instanced object of ldap with authentified connection.

        Raises:
            Exception: Error in the authentication with server by something reason

        """

        try:

            self.conn = ldap.initialize("ldap://"+self.ip+":"+self.port)
            self.conn.simple_bind(self.dn, self._password)  # simple bind changed
            print self.conn.whoami_s()
        except:
            raise Exception('Error al conectar con el servidor')

    def ldapsearch(self, attrib_forsearch, attrib_toshow, **kwargs):
        """
        ldapsearch(self, attrib_forsearch, attrib_toshow, **kwargs) -> list

        This functions allow get data list of a object in the active directory, based in a search of a information
        that then is filtered to taste by user.

        Args:
            attrib_forsearch (str): Attribute with value for search all data.
            attrib_toshow (list of str): Filter data according to attributes.
            **kwargs: Domain if need be changed (optional).

        Attributes:
            attrib_forsearch (str): Its composed by two importants parts.
                firts, the attribute of domain for try search, secondly, the value for search all data.
            attrib_toshow (list): Use attributes with comma separate what you need get.
            **kwargs: It is used for change default domain of search,
                you can use url as domain or distinguishedName, use domain='dn_or_url'.

        .. warning:: in case of use **kwargs as domain with DN, no use spaces, be sure to separate only by commas

        Returns:
            list from getsearch().

        Raises:
            SyntaxError: In case that you kwarg domain is corrupted.

        .. note:: search_this and show_this module could help you
        .. seealso:: https://msdn.microsoft.com/en-us/library/windows/desktop/ms675090(v=vs.85).aspx

        Example:
            should use authentified object of myldap and then try search:
            without help modules.

            >>> auth_object.ldapsearch('mail=mailfor@search.com', ['distinguishedName'])
            [['distinguishedName', 'CN=name_user,CN=Users,DC=owner,DC=local']]

            with show_this and search_this functions.

            >>> auth_object.ldapsearch(search_by_mail('mailfor@search.com'), show_dn())
            [['distinguishedName', 'CN=name_user,CN=Users,DC=owner,DC=local']]

        """

        try:
            self.conn.protocol_version = ldap.VERSION3
            self.conn.set_option(ldap.OPT_REFERRALS, 0)

            if 'domain' in kwargs:
                if is_domain_dn(kwargs['domain']):  # verify if is a valid domain
                    self.domain = kwargs['domain']
                elif is_domain_url(kwargs['domain']):  # verify if is a valid url domain
                    self.domain = to_distinguished_name(kwargs['domain'])  # convert url domain to dn
                else:
                    raise SyntaxError('Has escrito un dominio invalido, asegurate de no tener espacios,'
                                      'por ejemplo dc=ejemplo,dc=com')

            result = self.conn.search_s(self.domain,
                                        ldap.SCOPE_SUBTREE,
                                        attrib_forsearch)

            _resultssearch = [entry for dn, entry in result if isinstance(entry, dict)]
            if not _resultssearch:  # if is empty return 0 because not found the search...
                # similar that, "if results == []"
                _resultssearch = 0
            else:
                _resultssearch = _resultssearch[0]  # _resultssearch[0] because need delete unnecessary []
                return self.getsearch(_resultssearch, attrib_toshow)
            # return results[0]
        finally:
            pass
            # self.conn.unbind(), this here can close the connection of ldap

    def ldapadd(self, domain=''):

        attrs = {}
        attrs['objectclass'] = ['top', 'organizationalRole', 'simpleSecurityObject']
        attrs['cn'] = 'replica'
        attrs['userPassword'] = 'aDifferentSecret'
        attrs['description'] = 'User object for replication using slurpd'

        ldif = modlist.addModlist(attrs)
        print attrs
        self.conn.add_s('cn=replica, cn=Users, dc=owner,dc=local', ldif)
        # self.conn.unbind()

    def getsearch(self, _resultssearch, attrib_toshow):
        """
        getsearch(self, _resultssearch, attrib_toshow) -> list

        Take the dictionary result of ldapsearch, and make reorganization in a list.

        Args:
            _resultssearch (dict): Iterable data.
            attrib_toshow (list of str): Filter data according to attributes.

        Attributes:
            _resultssearch (dict): It contains human readable data about search.
            attrib_toshow (list): Use attributes with comma separate what you need get.

        Returns:
            _foundit(list): Filtered list of dict of _resultssearch.

        Raises:
            LookupError: if didn't find something as a result of _resultssearch.

        """

        if _resultssearch != 0:
            _foundit = []
            # first of all take dict keys, which will be compared with attributes specified in (attributetosearch),
            # then add it to new list till loop end
            for key, data in _resultssearch.iteritems():
                for atrib in attrib_toshow:
                    if key.lower() == atrib.lower():  # convert to lower for insensitive case
                        _foundit.append([key, data[0]])  # data[0] because need delete unnecessary []
            print _foundit
            return _foundit
        else:
            raise LookupError('Lo sentimos lo que has buscado no ha sido encontrado')


#Nop = Myldap('192.168.0.23', 'cn=administradortest,cn=Users,dc=owner,dc=local', '123456789Xx')
#Nop.ldapsearch(search_by_mail('a@a.a'), show_dn())



#Nop.ldapadd()
#Nop = myldap('192.168.10.28', 'cn=Administrador,cn=Users,dc=ITFIPSALAS,dc=LOCAL', 'Itfip2015')
#print('fin')
#consulta = Nop.ldapsearch(search_by_name('admin'),domain='WWW.ITFIPSALAS.LOCAL')
#print Nop.getsearch(consulta,show_mail())


#Nop.ldapadd()

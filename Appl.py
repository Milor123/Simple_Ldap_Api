# /usr/bin/env python 2.7
# -*- coding: utf-8 -*-
import ldap
import ldap.modlist as modlist
import time
from functions.convert import is_domain_dn, is_domain_url,\
                              to_domain, to_distinguished_name

from functions.show_this import show_profile, show_mail,\
                                show_name, show_password,\
                                show_telephone_number, show_member_of,\
                                show_sensitive_data, show_dn

from functions.search_this import search_by_number, search_by_mail,\
                                  search_by_dn, search_by_dn,\
                                  search_by_name

from functions.decorators import requiere


class Myldap(object):
    """
    first of all, this module is specially created for active directory working of the university
    "Instituto Tolimense de Educacion Superior" (ITFIP). Our objective is to ease
    centralization of data through ldap protocol.

    This module establishes a connection to active directory, of Windows Server, by means of a user of domain,
    on top of that, allow data query, and other functions such as, add, modify, compare data

    Attributes:
        | conn (instance): instanced connection of ldap object.
        | domain (str): DN converted to domain with helpful method.
    """

    def __init__(self, ip, dn, _password, port='389'):
        """
        In the constructor define the sensitive data for Active Directory connection, then call to _connect().

        Args:
            | ip (str): ip address.
            | dn (str): Distinguished Name.
            | _password (str): User password.
            | port (str): connection port.

        Attributes:
            | ip (str): ip address of domain server.
            | dn (str): is a sequence of relative distinguished names (RDN) connected by commas, thus must contain
                administrator user locate and Domain.
            | _password (str): you must specify an adminstrator user of Domain in the Active Directory.
            | port (str): Active Directory Domain Services Port.

            .. seealso::
                | https://msdn.microsoft.com/en-us/library/windows/desktop/aa366101%28v=vs.85%29.aspx

                https://technet.microsoft.com/en-us/library/dd772723%28v=ws.10%29.aspx

        Examples:
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
        self.base = dn
        self._connect()

    def _connect(self):
        """
        This method will create an instanced object of ldap with authentified connection.

        Raises:
            Exception: Error in the authentication with server by some reason

        """

        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        self.conn = ldap.initialize("ldap://"+self.ip+":"+self.port)

        self.conn.set_option(ldap.OPT_REFERRALS,0)
        self.conn.set_option(ldap.OPT_PROTOCOL_VERSION,3)
        self.conn.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
        self.conn.set_option(ldap.OPT_X_TLS_DEMAND,True)
        self.conn.set_option(ldap.OPT_DEBUG_LEVEL,255)
        try:
            time.sleep(0.5)
            self.conn.simple_bind(self.dn, self._password)  # simple bind changed
            print self.conn.whoami_s()
        except:
            raise Exception('Error al conectar con el servidor')

    def ldapsearch(self, attrib_forsearch, attrib_toshow, **kwargs):
        """
        ldapsearch(self, attrib_forsearch, attrib_toshow, **kwargs) -> list

        This functions allow to get data list of an object in the active directory, based on a search of a information
        that then is filtered according to user's needs.

        Args:
            | attrib_forsearch (str): Attribute with value for search all data.
            | attrib_toshow (list of str): Filter data according to attributes.
            | **kwargs: Domain if need be changed (optional).

        Attributes:
            | attrib_forsearch (str): It's composed by two importants parts.
                firts, the attribute of domain for try search, secondly, the value for searching all the data.
            | attrib_toshow (list): Use attributes with comma separate what you need to get.
            | **kwargs: It is used for changing default domain of search,
                you can use url as domain or distinguishedName, use domain='dn_or_url'.

            .. warning:: in case of use **kwargs as domain with DN, don't use spaces, be sure to separate only by commas
            .. note:: search_this and show_this module could help you
            .. seealso:: https://msdn.microsoft.com/en-us/library/windows/desktop/ms675090(v=vs.85).aspx
        Returns:
            list from getsearch().

        Raises:
            SyntaxError: In case that your kwarg domain is corrupted.

        Examples:
            | Should use authentified object of myldap and then try search:
            | Without help modules:

            >>> auth_object.ldapsearch('mail=mailfor@search.com', ['distinguishedName'])
            [['distinguishedName', ['CN=name_user,CN=Users...']]]

            With show_this and search_this functions.

            >>> auth_object.ldapsearch(search_by_mail('mailfor@search.com'), show_dn())
            [['distinguishedName', ['CN=name_user,CN=Users...]]]

            Incidentally we must not forget, this can find multiple values, to give an illustration of what I mean,
            will try to get a memberOf data in admintratortest:

            >>> auth_object.ldapsearch(search_by_mail('administradortest@owner.local'), show_member_of())
            [['memberOf', ['CN=blabla ,CN=Users,DC=owner...', 'CN=Admins. blabla,CN=Users,DC=owner...', 'CN= blablabla,DC=owner,DC=local']]]

        Example attributes:
            auth_object(Instance): refers to authenfied instace with administrator data
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

            print result
            _resultssearch = [entry for dn, entry in result if isinstance(entry, dict)]
            if not _resultssearch:  # if it is empty return 0 because it did not find the search...
                # similar that, "if results == []"
                _resultssearch = 0
            else:
                _resultssearch = _resultssearch[0]  # _resultssearch[0] because need delete unnecessary []
                return self.getsearch(_resultssearch, attrib_toshow)
            # return results[0]
        finally:
            pass
            # self.conn.unbind(), this here can close the connection of ldap

    def ldapadd(self, objectdn, attrs_dict):
        """
        This function can add an object in Active Directory, which needs a DN and the attributes object

        Args:
            | objectdn (str): DistinguishedName for new object
            | attrs_dict: Dictionary with info object

        Raises:
            | ValueError: Object or user already exist
            | NameError: From my point of view, usually this is brought about of different information,
                which is specified in the dictionary and objectdn, in other words,
                if you cn in the DN isn't same than cn in the dictionary, the error occurs
        Returns:
            Spanish message that shows, that the object has been created correctly

        Examples:
            | Create a dict with data object:

            >>> attrs = {}
            >>> attrs['objectclass'] = ['top', 'organizationalPerson', 'Person', 'user']
            >>> attrs['cn'] = 'userman'
            >>> attrs['userPassword'] = 'Secret'
            >>> attrs['description'] = 'I am new user xDDD'
            >>> auth_object.ldapadd('cn=userman,cn=Users,dc=owner,dc=local', attrs)
            The object has been created correctly
        """
        ldif = modlist.addModlist(attrs_dict)  # convert dict with special parse of ldap

        try:
            self.conn.add_s(objectdn, ldif)
            return 'El objeto ha sido creado correctamente'
        except ldap.ALREADY_EXISTS as e:
            raise ValueError('El objeto ya existe ::', e)
        except ldap.INVALID_DN_SYNTAX as e:
            raise NameError('Puede que hayas espeficiado un objeto diferente en el diccionario que en el DN ::', e)

    def ldapmodify(self, objectdn, attrs_new):
        """
        This function can modify an object in Active Directory, taking an object and stipulate new data for attributes

        Args:
            | objectdn (str): DistinguishedName of object to modify
            | attrs_new (dict): Acive Directory Attributes dicctionary with value need for modify

        Examples:
            go to change current telephoneNumber.

            >>> auth_object.ldapmodify('cn=administratortest,cn=Users,dc=owner,dc=local', {'telephoneNumber': '515336'})

            | In this moment us number should be 515336.
            | could check this with:
            >>> auth_object.ldapsearch(search_by_mail('administradortest@owner.local'), show_telephone_number())
            [['telephoneNumber' ['515336']]]

            .. Warning::
                | Modify attributes with multiple data are experimental code, don't use it
                | if you need add multiple data, use comma to separate in a list for the value, one example could be:
                >>> auth_object.ldapmodify('cn=administratortest...', {'memberOf': ['Group_of_blabla','blablabla','More_blabla']})
        """

        attrs_old = {}
        for key, value in attrs_new.iteritems():
            if isinstance(value, list):
                temporallist = []
                for x in value:
                    temporallist.append('x')
                attrs_old[key] = temporallist
            else:
                attrs_old[key] = 'x'  # this is the old value with a random value as x, for replace all

        ldif = modlist.addModlist(attrs_old, attrs_new)
        print 'lel', ldif
        self.conn.modify_s(objectdn, ldif)

    def getsearch(self, _resultssearch, attrib_toshow):
        """
        getsearch(self, _resultssearch, attrib_toshow) -> list

        Take the dictionary result of ldapsearch, and make reorganization in a list.

        Args:
            | _resultssearch (dict): Iterable data.
            | attrib_toshow (list of str): Filter data according to attributes.

        Attributes:
            | _resultssearch (dict): It contains human readable data about search.
            | attrib_toshow (list): Use attributes with comma separate what you need to get.

        Returns:
            | _foundit(list): Filtered list of dict of _resultssearch.

        Raises:
            | LookupError: if it didn't find something as a result of _resultssearch.

        """

        if _resultssearch != 0:
            _foundit = []
            # first of all take dict keys, which will be compared with attributes specified in (attributetosearch),
            # then add it to new list till loop end
            for key, data in _resultssearch.iteritems():
                for atrib in attrib_toshow:
                    if key.lower() == atrib.lower():  # convert to lower for insensitive case
                        _foundit.append([key, data])  # Note: not use data[0] because could have more information
            return _foundit
        else:
            raise LookupError('Lo sentimos lo que has buscado no ha sido encontrado')

    def ldapcompare_fast(self, dn, attr, value):
        """
        ldapcompare_fast(self, dn, attr, value) -> boolean

        Args:
            | dn (str): Object DN.
            | attr (str): Attribute to compare.
            | value (str): Value for compare.

        Returns:
            | True if the values are same.
            | False if the values no match.

        References:
            https://www.packtpub.com/books/content/configuring-and-securing-python-ldap-applications-part-2

        Examples:
            | if the xD user have phoneNumver value = 11257.
            >>> auth_object.ldapcompare_fast('cn=xD,cn=Users,dc=owner,dc=local','telephoneNumber', '5559971')
            False

            >>> auth_object.ldapcompare_fast('cn=xD,cn=Users,dc=owner,dc=local','telephoneNumber', '11257')
            True

        .. warning::
            * Don't use with attributes of multiple values as memberOf, could throw false positive.
            * Don't use spaces in DN, be sure to separate only by comma.
        """

        try:
            self.conn.result(self.conn.compare(dn, attr, value))
        except ldap.COMPARE_TRUE:
            return True
        except ldap.COMPARE_FALSE:
            return False

    def ldapcompar_advance(self, dn, attrvalue, dntocompare, attrvaluecompare):
        """
        ldapcompar_advance(self, dn, attrvalue, dntocompare, attrvaluecompare) -> boolean or string

        This method allows to compare two attribute values with DN.

        Args:
            dn (str): Firts object DN to compare.
            attrvalue (str): Firts attribute to compare.
            dntocompare (str): Second object DN to compare.
            attrvaluecompare (str): Second attribute to compare.

        Returns:
            | Both are empty' if the values of Both attributes are empty.
            | True if the values are same.
            | False if the values no match.

        .. warning::
                * Don't use with attributes of multiple values as memberOf, could throw false positive.
                * Don't use spaces in DN, be sure to separate only by comma.

        Examples:
            | Phones numbers compare with different users.
            >>> auth_object.compar_advance('cn=xD,cn=Users,dc=owner,dc=local','telephoneNumber',
            ...                            'cn=administradortest,cn=Users,dc=owner,dc=local','telephoneNumber')
            False

            | will use the same user. should be true or throw Both are empty if haven't data.
            >>> auth_object.compar_advance('cn=xD,cn=Users,dc=owner,dc=local','telephoneNumber',
            ...                            'cn=xD,cn=Users,dc=owner,dc=local','telephoneNumber')
            True
        """

        # use [attr] because need a list
        firt_value = self.ldapsearch(search_by_dn(dn), [attrvalue])
        second_value = self.ldapsearch(search_by_dn(dntocompare), [attrvaluecompare])
        if not firt_value and not second_value:
            return 'Both are empty'your

        if second_value:
            # [0][1][0], the firts is for enter in attribute, [1] for select value, [0] for enter in value
            second_value = second_value[0][1][0]
        else:
            second_value = ''
        return self.ldapcompare_fast(dn, attrvalue, second_value)

    def changePassword(self, user_dn, old_password, new_password):

        # Reset Password
        unicode_pass = unicode('\"' + str(new_password) + '\"', 'iso-8859-1')
        password_value = unicode_pass.encode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]

        self.conn.modify_s(user_dn, add_pass)

        # Its nice to the server to disconnect and free resources when done
        #.unbind_s()




#Nop = Myldap('192.168.0.17', 'cn=administradortest,cn=Users,dc=owner,dc=local', '123456789Xx')
#Nop.ldapmodify('cn=xD,cn=Users,dc=owner,dc=local', {'memberOf':'CN=Administradores,CN=Builtin,DC=owner,DC=local'})
#Nop.changePassword('cn=administradortest,cn=Users,dc=owner,dc=local','Mat@123123', '123456789Xx')
#print Nop.ldapsearch(search_by_dn('cn=administradortest,cn=Users,dc=owner,dc=local'), show_dn())

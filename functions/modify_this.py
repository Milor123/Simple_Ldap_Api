"""
Modify Functions
^^^^^^^^^^^^^^^^^^^
Use this in ldapmodify Function
"""


def modify_profile(displayname, mail, telephonenumber):
    """modify_profile() -> dict """
    return {'displayName': displayname, 'mail': mail, 'telephoneNumber': mail}


def modify_mail(mail):
    """modify_mail() -> dict """
    return {'mail': mail}


def modify_name(name):
    """modify_name() -> dict """
    return {'Name': name}


def modify_dn(dn):
    """modify_dn() -> dict """
    return {'distinguishedName': dn}


def modify_sensitive_data(useprincipalname, userpassword):
    """modify_sensitive_data() -> dict """
    return {'userPrincipalName': useprincipalname, 'userPassword': userpassword}


def modify_member_of(memberof):
    """modify_member_of() -> dict """
    return {'memberOf': memberof}

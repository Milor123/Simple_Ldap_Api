"""
Show Functions
^^^^^^^^^^^^^^^^^^^
Use this in ldapsearch Function
"""


def show_profile():
    """show_profile() -> list """
    return ['displayName', 'mail', 'telephoneNumber', 'physicalDeliveryOfficeName']


def show_mail():
    """show_mail() -> list """
    return ['mail']


def show_name():
    """show_name() -> list """
    return ['Name']


def show_dn():
    """show_dn() -> list """
    return ['distinguishedName']


def show_sensitive_data():
    """show_sensitive_data() -> list """
    return ['userPrincipalName', 'primaryGroupID', 'sAMAccountType', 'userPrincipalName','mail']


def show_member_of():
    """show_member_of() -> list """
    return ['memberOf']


def show_telephone_number():
    """show_telephone_number() -> list """
    return ['telephoneNumber']

def show_password():
    """show_password() -> list """
    return ['userPassword']
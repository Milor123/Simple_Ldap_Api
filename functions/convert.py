# /usr/bin/env python 2.7
"""
Convert and Verify Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note:: You should know about distinguished name (dn) and your structure
.. seealso:: https://msdn.microsoft.com/en-us/library/aa366101(v=vs.85).aspx
"""


def to_domain(dn):
    """
    to_domain(dn) -> String
    this function convert dn with only domainComponent to domain
    """
    import re
    dn = dn.split(',')
    domain = []
    dnsearch = re.compile(r'^dc=')
    for x in dn:
        if dnsearch.search(x):
            domain.append(x)
    domain = ','.join(domain)
    return domain


def to_distinguished_name(domain_url):
    """
    to_distinguished_name(domain_url) -> String
    this function convert domain to dn with only domainComponent
    """
    domain_url = domain_url.split('.')
    dn = []
    for x in domain_url:
        if not (x == 'www' or x == 'WWW'):
            dn.append('dc='+x)
    dn = ','.join(dn)
    return dn


def is_domain_dn(dn):
    """
    is_domain_dn(dn) -> boolean
    this function verify if you dn is a dn with only domainComponent
    """
    import re
    exp = r"((dc=[a-zA-Z0-9\-]+[\,]{1})+(dc=[a-zA-Z0-9\-]+)$)"
    dnsearch = re.compile(exp)
    if dnsearch.search(dn):
        return True
    else:
        return False


def is_domain_url(domain_url):
    """
    is_domain_url(domain_url) -> boolean
    this function verify if is url
    """
    import re
    www = re.compile(r"(([a-zA-Z0-9\-]+[\.]{1})+([a-zA-Z0-9\-]+)$)")
    if www.search(domain_url):
        return domain_url
    else:
        return False

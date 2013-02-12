import re
from collections import namedtuple

# This module based on rfc3986.

# Section 3.1. Scheme
# | URI scheme specifications must define their own syntax so that
# | all strings matching their scheme-specific syntax will also match
# | the <absolute-URI> grammar:
#
# | absolute-URI  = scheme ":" hier-part [ "?" query ]
#
# As we can see, <absolute-URI> not require all scheme-specific
# syntaxis to have fragment part. But as defined in section 2.2.,
# "#" one of the generic delimiters. It also defined as delimeter
# in many parts of rfc. As a result url can not contain char "#"
# without quoting even if it scheme-specific syntax not use "#":
#
# | If data for a URI component would conflict with a reserved
# | character's purpose as a delimiter, then the conflicting data
# | must be percent-encoded before the URI is formed.
#
_split_re = re.compile(r'''
    (?:([a-z][a-z0-9+\-.]*):)?  # scheme
    (?://                       # authority
        (?:([^/?\#@\[\]]*)@)?   # userinfo
        ([^/?\#]*)              # host:port
    )?
    ([^?\#]*)                   # path
    \??([^\#]*)                 # query
    \#?(.*)                     # fragment
    ''', re.VERBOSE | re.IGNORECASE | re.DOTALL).match

URLBase = namedtuple('URLBase', 'scheme host path query fragment userinfo port')

class URL(URLBase):
    __slots__ = ()

    def __new__(cls, url=None, scheme='', host='', path='', query='',
                fragment='', userinfo='', port=''):
        if url is not None:
            (scheme, userinfo, host,
             path, query, fragment) = _split_re(url).groups('')

            # We can not match port number in regexp. Host itself can contain
            # digits and ":"
            _port_idx = host.rfind(':')
            if _port_idx >= 0:
                _port = host[_port_idx + 1:]
                if not _port or _port.isdigit():
                    host, port = host[:_port_idx], _port

        # | Although schemes are case-insensitive, the canonical form
        # | is lowercase. An implementation should only produce lowercase
        # | scheme names for consistency.
        scheme = scheme.lower()

        # | Although host is case-insensitive, producers and normalizers
        # | should use lowercase for registered names and hexadecimal
        # |addresses for the sake of uniformity.
        # TODO: | while only using uppercase letters for percent-encodings
        host = host.lower()

        return tuple.__new__(cls, (scheme, host, path, query, fragment,
                                   userinfo, port))

__all__ = ['md5_digest']

import hashlib

def unicode_digest(hash_name, content):
    hasher = getattr(hashlib, hash_name)
    return hasher(content.encode('utf-8')).hexdigest().decode('ascii')

def md5_digest(content):
    return unicode_digest('md5', content)


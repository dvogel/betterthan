
__all__ = ('dict_mget', 'mget')


def dict_mget(thedict, keylist, default=None):
    d = thedict
    for k in keylist:
        if k in d:
            d = d.get(k)
        else:
            return default
    return d

mget = dict_mget


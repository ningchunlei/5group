__author__ = 'chunlei3'

def isEmpty(params,key):
    if not params.has_key(key):
        return True
    return params[key]==""

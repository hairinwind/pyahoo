from os import environ

def isDev():
    print('PYAHOO_ENV', environ.get('PYAHOO_ENV'))
    return environ.get('PYAHOO_ENV') == 'dev'
from os import environ

def isDev():
    print(environ.get('PYAHOO_ENV'))
    return environ.get('PYAHOO_ENV') == 'dev'
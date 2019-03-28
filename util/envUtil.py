from os import environ

def isDev():
    return getPyahooEnv() == 'dev'

def getPyahooEnv():
    return environ.get('PYAHOO_ENV')
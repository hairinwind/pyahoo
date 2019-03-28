from util.envUtil import *

def test_getPyahooEnv():
    assert getPyahooEnv() == 'dev'
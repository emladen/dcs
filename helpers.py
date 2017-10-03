'''
Created on Oct 2, 2017

@author: root
'''

import web
from web.webapi import seeother
from web import form

g_user = 'admin'
g_password = 'admin'

def check_login(redirect=False):
    """
    Check login.
    """
    qdict = web.input()
    
    try:
#         if gv.sd['ipas'] == 1:
#             return True
    
        if web.config._session._initializer['user'] == 'admin':
            return True
    except KeyError:
        pass
    
    if ('password' in qdict) and ('username' in qdict):
        if validate_login(qdict['username'], qdict['password']):
            return True
        if redirect:
            raise web.unauthorized()
        return False
    
    
#     if 'pw' in qdict:
#         if gv.sd['password'] == password_hash(qdict['pw'], gv.sd['salt']):
#             return True
#         if redirect:
#             raise web.unauthorized()
#         return False
    
    if redirect:
        raise web.seeother('/login')
    return False

def validate_login(user, password):
    #return (user, password) [user == g_user and password == g_password]
    if user == g_user and password == g_password:
        return True
    else:
        return False

def toogle_power_status(status):
    if status == "power-off":
        return "power-on"
    else:
        return "power-off"
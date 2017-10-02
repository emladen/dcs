'''
Created on Sep 30, 2017

@author: erkic
'''

import web
from web import form
from dcs import render, template_globals
from helpers import *


class ProtectedPage():
    def __init__(self):
        check_login(True)
#        WebPage.__init__(self)


### Web pages ######################
class index(ProtectedPage):
    def GET(self):
        if web.config.get('_session') is None:
            user = 'test'
        return render.home()

# my3form = form.Form(
#     form.Textbox("ime"),
#     form.Password("password"))
   
    
class login:
    def GET(self):
        t = 1
        return render.login(True)
#         form2 = my3form()
#         return render.login2(form2)
    
    def POST(self):
        log_dict = web.input()
        if not validate_login(log_dict.get('username'), log_dict.get('password')):
            # shuld return information for repair
            return render.login(False)
        else:
            web.config._session._initializer['user'] = 'admin'
            template_globals['user'] = 'admin'
            #report_login()
            raise web.seeother('/home')

class logout:
    def GET(self):
        pass
        #web.config._session.user = 'anonymous'
        web.config._session._initializer['user'] = 'anonymous'
        raise web.seeother('/')       


class home(ProtectedPage):
    def GET(self):
        x = 5
        pass
        user = web.config._session._initializer['user']
        if web.config.get('_session') is None:
            web.config._session.user = 'anonymous'
        #session.user = 'admin2'
        return render.home()

class about(ProtectedPage):
    def GET(self):
        return render.about()
        #return render.home2()

class safetyinstructions(ProtectedPage):
    def GET(self):
        return render.safety()    
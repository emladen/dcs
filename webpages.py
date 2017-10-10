'''
Created on Sep 30, 2017

@author: erkic
'''

import web
from dcs import render, template_globals, pw_system_globals
from helpers import *
from gpio_pins import *


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
        #web.config._session.count += 1
        return render.login(True)
#         form2 = my3form()
#         return render.login2(form2)
    
    def POST(self):
        log_dict = web.input()
        if not validate_login(log_dict.get('username'), log_dict.get('password')):
            # shuld return information for repair
            return render.login(False)
        else:
            web.config._session['user'] = 'admin'
            template_globals['user'] = 'admin'
            #report_login()
            raise web.seeother('/home')

class logout:
    def GET(self):
        web.config._session['user'] = 'anonymous'
        web.config._session.kill()
        raise web.seeother('/')       


class home(ProtectedPage):
    def GET(self):
        user = web.config._session['user']
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
    
class emergency_turnoff(ProtectedPage):
    
    def GET(self):
        for key in pw_system_globals.keys():
            pw_system_globals[key] = 'power-off'
        
        turn_gpio_off()
        raise web.seeother('/')
        
class change_motor_position(ProtectedPage):
    
    def GET(self):
        qdict = web.input()
        
        motor_pos = {
             'mot_pos0'  : 'power-off',
             'mot_pos90'   : 'power-off',
             'mot_pos180'   : 'power-off',
             'mot_pos270'   : 'power-off',
            }
        try:
            for key in qdict.keys():
                for pos in ["0", "90", "180", "270"]:
                    if key in motor_pos.keys():
                        if key <> ('mot_pos' + pos): 
                            pw_system_globals["mot_pos" + pos] = "power-off"
                        elif key == ('mot_pos' + pos):
                            pw_system_globals["mot_pos" + pos] = "power-on"
        except Exception:
            pass
            
            
        #return render.home()
        raise web.seeother('/')  # Send browser back to home page     
    
class change_values(ProtectedPage):
    """Save controller values, return browser to home page."""

    def GET(self):
        qdict = web.input()

        for key in qdict.keys():
            try:
                if key in pw_system_globals.keys():
                    pw_system_globals[key] = toogle_power_status(qdict[key])
                    if pw_system_globals[key] == "power-on":
                        turn_reley_on_by_name(key)
                    elif pw_system_globals[key] == "power-off":
                        turn_reley_off_by_name(key)
            except Exception:
                pass
        #return render.home()
        raise web.seeother('/')  # Send browser back to home page            
 
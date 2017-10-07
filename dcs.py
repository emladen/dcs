import web
from webpages import *
from urls import *
from gpio_pins import *

web.config.debug = False
app = web.application(urls, globals())
if web.config.get('_session') is None:
    web.config._session = web.session.Session(app, web.session.DiskStore('sessions'),
                                              initializer={'user': 'anonymous'})
    
pw_system_globals = {
    'relay1'    : 'power-off',
    'relay2'    : 'power-off',
    'relay3'    : 'power-off',
    'relay4'    : 'power-off',
    'relay5'    : 'power-off',
    'relay6'    : 'power-off',
    'relay7'    : 'power-off',
    'relay8'    : 'power-off',
    'relay9'    : 'power-off',
    'mot_pos0'  : 'power-off',
    'mot_pos90'   : 'power-off',
    'mot_pos180'   : 'power-off',
    'mot_pos270'   : 'power-off',
    }
template_globals = {
    'app_path': lambda p: web.ctx.homepath + p,
    'session': web.config._session,
    'web': web,
    'user': web.config._session._initializer['user'],
    'pw_system': pw_system_globals
}
render = web.template.render('templates/', globals=template_globals)

if __name__ == "__main__": 
    app.run()    
import web
from urls import *
from gpio_pins import *
from helpers import setup_database

web.config.debug = False
app = web.application(urls, globals())
#db = web.database(dbn='sqlite', 'db')
if web.config.get('_session') is None:
    web.config._session = web.session.Session(app, web.session.DiskStore('sessions'),
                                              initializer={'user': 'anonymous', 'count': 0})
    
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
    'mot_rot_90l'    : 'power-off',
    'mot_rot_10l'    : 'power-off',
    'mot_rot_10r'    : 'power-off',
    'mot_rot_90r'    : 'power-off',            
    }

setup_database()
web.config._session['user'] = 'anonymous'
template_globals = {
    'app_path': lambda p: web.ctx.homepath + p,
    'session': web.config._session,
    'web': web,
    'user': web.config._session['user'],
    'pw_system': pw_system_globals
}
render = web.template.render('templates/', globals=template_globals)


if __name__ == "__main__": 
    app.run()    
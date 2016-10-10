import os.path
from komlog.komws2 import web_modules

DIRNAME = os.path.dirname(__file__)
SETTINGS = {
            'template_path':os.path.join(DIRNAME, "templates"),
            'static_path':'/static/',
            'cookie_secret': 'FC+EWT0sRh+iDGsqD4xvcm6UkRUw4UuWvsKeq8x8aHk=',
            'xsrf_cookies': False, #hay problemas con los procesos que se conecta por POST que no pertenecen al Frontal Web... hay que revisarlo
            'login_url': '/login',
            'ui_modules': web_modules.MODULES,
}


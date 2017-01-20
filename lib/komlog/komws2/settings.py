import os.path
from komlog.komws2 import web_modules

DIRNAME = os.path.dirname(__file__)
SETTINGS = {
            'template_path':os.path.join(DIRNAME, "templates"),
            'static_path':'/static/',
            'cookie_secret': 'FC+EWT0sRh+iDGsqD4xvcm6UkRUw4UuWvsKeq8x8aHk=',
            'jwt_secret':'ASDASVCasvdsagj3483)(jhasdf_//hasdf-_=$|asdf3',
            'xsrf_cookies': True,
            'login_url': '/login',
            'ui_modules': web_modules.MODULES,
}


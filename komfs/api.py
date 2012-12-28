'''
copyright jcazor
date 2012-12-14
'''

import os

samples_path = '/komlog/samples/'

def create_sample(name, data, encoding):
    filename = os.path.join(samples_path,str(name))
    try:
        file_handler = open(filename,'w')
        udata = data.decode(encoding)
        file_handler.write(udata.encode('utf8'))
        file_handler.close()
    except:
        return False
    else:
        return True

def get_file_content(name):
    try:
        content = open(name,'r').read()
        ucontent = content.decode('utf8')
    except Exception:
        return None
    else:
        return ucontent

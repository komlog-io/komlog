'''
copyright jcazor
date 2012-12-14
'''

import os

samples_path = '/komlog/samples/'

def create_sample(name, data, encoding):
    filename = os.path.join(samples_path,str(name))
    file_handler = open(filename,'w')
    udata = data.decode(encoding)
    file_handler.write(udata.encode('utf8'))
    file_handler.close()
    return True

def get_file_content(name, encoding='utf8'):
    content = open(name,'r').read()
    ucontent = content.decode(encoding) #unicode
    return ucontent

'''
copyright jcazor
date 2012-12-14
'''

import os

samples_path = '/home/jcazor/komlog/samples/pending'

def create_sample(name, data):
    filename = os.path.join(samples_path,str(name))
    file_handler = open(filename,'w')
    file_handler.write(data.encode('utf8'))
    file_handler.close()
    return True

def get_file_content(name):
    content = open(name,'r').read()
    ucontent = content.decode('utf8') #unicode
    return ucontent

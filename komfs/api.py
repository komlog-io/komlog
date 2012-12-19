'''
copyright jcazor
date 2012-12-14
'''

import os

samples_path = '/komlog/samples/'

def create_sample(name, data):
    filename = os.path.join(samples_path,str(name))
    try:
        file_handler = open(filename,'w')
        lenght = file_handler.write(data)
        file_handler.close()
    except:
        return False
    else:
        return True

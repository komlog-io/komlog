'''
copyright jcazor
date 2012-12-14
'''


def create_sample(file_name, data):
    file_handler = open(file_name,'w')
    file_handler.write(data.encode('utf8'))
    file_handler.close()
    return True

def get_file_content(name):
    content = open(name,'r').read()
    ucontent = content.decode('utf8') #unicode
    return ucontent

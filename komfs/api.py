'''
copyright jcazor
date 2012-12-14
'''

from komfig import logger

def create_sample(file_name, data):
    logger.logger.debug('creating file: '+str(file_name))
    file_handler = open(file_name, mode='w', encoding='utf-8')
    logger.logger.debug('storing content')
    file_handler.write(data)
    file_handler.close()
    return True

def get_file_content(name):
    logger.logger.debug('opening file: '+str(name))
    content = open(name, mode='r', encoding='utf-8').read()
    return content

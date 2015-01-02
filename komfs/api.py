'''
copyright jcazor
date 2012-12-14
'''

from komfig import logger

def create_sample(filename, data):
    try:
        file_handler = open(filename, mode='w', encoding='utf-8')
        file_handler.write(data)
        file_handler.close()
    except Exception as e:
        logger.logger.exception('Exception storing content in '+str(filename)+':  '+str(e))
        return False
    else:
        return True

def get_file_content(filename):
    try: 
        logger.logger.debug('opening file: '+str(filename))
        content = open(filename, mode='r', encoding='utf-8').read()
    except Exception as e:
        logger.logger.exception('Exception reading content from '+str(filename)+':  '+str(e))
        return None
    return content

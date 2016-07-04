'''
copyright jcazor
date 2012-12-14
'''


def create_sample(filename, data):
    fd=None
    try:
        fd= open(filename, mode='w', encoding='utf-8')
        fd.write(data)
    except Exception as e:
        return False
    else:
        return True
    finally:
        if fd:
            fd.close()

def get_file_content(filename):
    fd=None
    try: 
        fd=open(filename, mode='r', encoding='utf-8')
        content = fd.read()
        return content
    except Exception as e:
        return None
    finally:
        if fd:
            fd.close()


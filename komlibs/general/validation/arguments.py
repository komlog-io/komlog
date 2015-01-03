'''

This library is for implementing functions for argument validation

'''

import re
import uuid


NOTKOMLOGIDCHAR=re.compile('[^a-zA-Z0-9\-._]')
NOTKOMLOGDESCCHAR=re.compile('[^ a-zA-Z0-9\-._@#!$%&+=]')
NOTPASSWORD=re.compile('''[^a-zA-Z0-9!#$%&'*+/=?^_`{|}~":;,.<>\\-]''')
NOTPUBKEY=re.compile('[^ a-zA-Z0-9\-\+/\n]')
NOTVERSION=re.compile('[^ a-zA-Z0-9\-\+/:\._]')
NOTCODE=re.compile('[^a-zA-Z0-9]')
WHITESPACES=re.compile(' ')
ASCII=re.compile('a-zA-Z')
NUMBERS=re.compile('0-9')
EMAIL=re.compile('''^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$''')

def is_valid_username(argument):
    if not isinstance(argument,str):
        return False
    if NOTKOMLOGIDCHAR.search(argument):
        return False
    return True

def is_valid_agentname(argument):
    if not isinstance(argument,str):
        return False
    if NOTKOMLOGDESCCHAR.search(argument):
        return False
    return True

def is_valid_datasourcename(argument):
    if not isinstance(argument,str):
        return False
    if NOTKOMLOGDESCCHAR.search(argument):
        return False
    return True

def is_valid_datapointname(argument):
    if not isinstance(argument,str):
        return False
    if NOTKOMLOGDESCCHAR.search(argument):
        return False
    return True

def is_valid_datasource_content(argument):
    if not isinstance(argument,str):
        return False
    return True

def is_valid_password(argument):
    if not isinstance(argument,str):
        return False
    if NOTPASSWORD.search(argument):
        return False
    return True

def is_valid_email(argument):
    if not isinstance(argument,str):
        return False
    if EMAIL.search(argument):
        return True
    return False

def is_valid_code(argument):
    if not isinstance(argument,str):
        return False
    if NOTCODE.search(argument):
        return False
    return True

def is_valid_pubkey(argument):
    if not isinstance(argument,str):
        return False
    if NOTPUBKEY.search(argument):
        return False
    return True

def is_valid_version(argument):
    if not isinstance(argument,str):
        return False
    if NOTVERSION.search(argument):
        return False
    return True

def is_valid_uuid(argument):
    if isinstance(argument, uuid.UUID):
        return True
    return False

def is_valid_dict(argument):
    if isinstance(argument, dict):
        return True
    return False

def is_valid_bool(argument):
    if isinstance(argument, bool):
        return True
    return False

def is_valid_string_int(argument):
    if isinstance(argument,str):
        try:
            number=int(argument)
            return True
        except Exception:
            return False
    else:
        return False

def is_valid_date(argument):
    if isinstance(argument, uuid.UUID) and argument.version==1:
        return True
    return False

def is_valid_hexcolor(argument):
    if not isinstance(argument,str):
        return False
    if not len(argument)==7: #contamos el caracter '#'
        return False
    hexarray=argument.split('#')[-1]
    if not len(hexarray)==6:
        return False
    for index in [0,2,4]:
        hexcolor=hexarray[index:index+2]
        try:
            if not int('0x'+hexcolor,0)>=0 or not int('0x'+hexcolor,0)<256:
                return False
        except Exception:
            return False
    return True


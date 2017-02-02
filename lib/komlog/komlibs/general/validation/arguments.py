'''

This library is for implementing functions for argument validation

'''

import re
import uuid
import decimal
import pandas as pd
from komlog.komlibs.general.crypto import crypto


STR_MAX_LENGTH=256
USERNAME=re.compile('^([a-z0-9\-_]+\.)*[a-z0-9\-_]+(?!\s)$', re.UNICODE)
USERNAMEWITHCAP=re.compile('^([a-zA-Z0-9\-_]+\.)*[a-zA-Z0-9\-_]+(?!\s)$', re.UNICODE)
DESC=re.compile('^[ a-zA-Z0-9\-\._@#!\(\):/$%&+=]+(?!\s)$', re.UNICODE)
SPACEONENDS=re.compile('^\s|\s$', re.UNICODE)
URI=re.compile('^([a-zA-Z0-9\-_]+\.)*[a-zA-Z0-9\-_]+(?!\s)$', re.UNICODE)
GLOBALURI=re.compile('^([a-zA-Z0-9\-_]+\.)*[a-zA-Z0-9\-_]+:([a-zA-Z0-9\-_]+\.)*[a-zA-Z0-9\-_]+(?!\s)$', re.UNICODE)
RELURI=re.compile('^([a-zA-Z0-9\-_]+\.\.?)*[a-zA-Z0-9\-_]+(?!\s)$', re.UNICODE)
NOTVERSION=re.compile('[^ a-zA-Z0-9\-\+/:\._]')
CODE=re.compile('^[a-zA-Z0-9]+$')
WHITESPACES=re.compile(' ')
ASCII=re.compile('a-zA-Z')
NUMBERS=re.compile('0-9')
STRINGNUMBER=re.compile('^[+-]?([0-9]*\.)?[0-9]+([e|E][-|+]?[0-9]+)?(?!\s)$', re.UNICODE)
EMAIL=re.compile('''^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$''')
EMAILWITHCAPS=re.compile('''^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$''')
ISODATE=re.compile('^((?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$')

def is_valid_username(argument):
    if not isinstance(argument,str):
        return False
    if len(argument)<=STR_MAX_LENGTH and USERNAME.search(argument):
        return True
    return False

def is_valid_username_with_caps(argument):
    if not isinstance(argument,str):
        return False
    if len(argument)<=STR_MAX_LENGTH and USERNAMEWITHCAP.search(argument):
        return True
    return False

def is_valid_agentname(argument):
    if not isinstance(argument,str):
        return False
    if len(argument)>STR_MAX_LENGTH or len(argument) == 0:
        return False
    if SPACEONENDS.search(argument):
        return False
    return True

def is_valid_datasourcename(argument):
    if not isinstance(argument,str):
        return False
    if DESC.search(argument):
        return True
    return False

def is_valid_datapointname(argument):
    if not isinstance(argument,str):
        return False
    if DESC.search(argument):
        return True
    return False

def is_valid_widgetname(argument):
    if not isinstance(argument,str):
        return False
    if len(argument)>STR_MAX_LENGTH or len(argument) == 0:
        return False
    if SPACEONENDS.search(argument):
        return False
    return True

def is_valid_dashboardname(argument):
    if not isinstance(argument,str):
        return False
    if len(argument)>STR_MAX_LENGTH or len(argument) == 0:
        return False
    if SPACEONENDS.search(argument):
        return False
    return True

def is_valid_circlename(argument):
    if not isinstance(argument,str):
        return False
    if len(argument)<=STR_MAX_LENGTH and len(argument) > 0 and DESC.search(argument):
        return True
    return False

def is_valid_uri(argument):
    if not isinstance(argument,str):
        return False
    if URI.search(argument):
        return True
    return False

def is_valid_global_uri(argument):
    if not isinstance(argument,str):
        return False
    if GLOBALURI.search(argument):
        return True
    return False

def is_valid_relative_uri(argument):
    if not isinstance(argument,str):
        return False
    if RELURI.search(argument):
        return True
    return False

def is_valid_datasource_content(argument):
    if isinstance(argument, str) and len(argument.encode('utf-8'))<=2**17:
        return True
    return False

def is_valid_datapoint_content(argument):
    try:
        num=decimal.Decimal(argument)
        int(num)
        return True
    except (decimal.InvalidOperation, ValueError, TypeError, OverflowError):
        return False

def is_valid_string(argument):
    if not isinstance(argument,str):
        return False
    return True

def is_valid_bytes(argument):
    if isinstance(argument,bytes):
        return True
    return False

def is_valid_password(argument):
    if isinstance(argument,str) and len(argument)>=6 and len(argument)<=256:
        return True
    return False

def is_valid_email(argument):
    if not isinstance(argument,str):
        return False
    if EMAIL.search(argument):
        return True
    return False

def is_valid_email_with_caps(argument):
    if not isinstance(argument,str):
        return False
    if EMAILWITHCAPS.search(argument):
        return True
    return False

def is_valid_code(argument):
    if isinstance(argument,str):
        try:
            argument.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False
    return False

def is_valid_pubkey(argument):
    pubkey=crypto.load_public_key(argument)
    if pubkey and pubkey.key_size >= 4096:
        return True
    return False

def is_valid_version(argument):
    if not isinstance(argument,str):
        return False
    if NOTVERSION.search(argument):
        return False
    return True

def is_valid_hex_uuid(argument):
    try:
        u=uuid.UUID(argument)
        if u.version==4:
            return True
        else:
            return False
    except Exception:
        return False

def is_valid_hex_date(argument):
    try:
        u=uuid.UUID(argument)
        if u.version==1:
            return True
        else:
            return False
    except Exception:
        return False

def is_valid_isodate(argument):
    if isinstance(argument, str) and ISODATE.search(argument):
        try:
            t=pd.Timestamp(argument)
            if t.timestamp()<0:
                return False
            return True
        except (ValueError,pd.tslib.OutOfBoundsDatetime):
            return False
    elif isinstance(argument, pd.Timestamp):
        return True
    return False

def is_valid_int(argument):
    if isinstance(argument, int) and argument>=0:
        return True
    else:
        return False

def is_valid_timestamp(argument):
    if (isinstance(argument,int) or isinstance(argument,float)) and argument >= 0 and argument <= 2**32-1:
        return True
    return False

def is_valid_sequence(argument):
    return is_valid_hex_date(argument)

def is_valid_uuid(argument):
    if isinstance(argument, uuid.UUID) and argument.version==4:
        return True
    return False

def is_valid_dict(argument):
    if isinstance(argument, dict):
        return True
    return False

def is_valid_set(argument):
    if isinstance(argument, set):
        return True
    return False

def is_valid_list(argument):
    if isinstance(argument, list):
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
            if number>=0:
                return True
            else:
                return False
        except Exception:
            return False
    return False

def is_valid_string_float(argument):
    if isinstance(argument,str):
        try:
            number=float(argument)
            if number>=0:
                return True
            else:
                return False
        except Exception:
            return False
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

def is_valid_challenge(argument):
    if not isinstance(argument, str):
        return False
    try:
        b=bytes().fromhex(argument)
    except Exception:
        return False
    else:
        if len(b)==32:
            return True
        else:
            return False



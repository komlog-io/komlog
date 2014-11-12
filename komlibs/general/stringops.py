#coding: utf-8

'''

library for various general functions used along the code
related with string management

2013/07/30

'''

import string
import random

def get_randomstring(size=6, chars=string.ascii_uppercase + string.digits):
    return ''+''.join(random.choice(chars) for x in range(size))

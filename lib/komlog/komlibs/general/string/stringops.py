'''

library for various general functions used along the code
related with string management

2013/07/30

'''

import string
import random

def get_randomstring(length=6, chars=string.ascii_letters + string.digits + '-_'):
    return ''+''.join(random.SystemRandom().choice(chars) for x in range(length))

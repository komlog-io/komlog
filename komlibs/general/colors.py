#coding:UTF-8
'''
This library implements some color functions

'''

import random

def get_random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())


#coding:UTF-8
'''
This library implements some color functions

'''


def get_randomcolor():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def validate_hexcolor(color):
    if not len(color)==7: #contamos el caracter '#'
        return False
    hexarray=color.split('#')[-1]
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


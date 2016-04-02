'''
This package has numeric function and classes

2013/08/08
jcazor
'''
import math

def relevanceweight(vardict):
    weights={}
    elements={}
    totalelements=0
    for key in vardict:
        lenght=float(len(vardict[key]))
        elements[key]=lenght
        totalelements+=lenght
    for key in vardict:
        weights[key]=math.pow(elements[key],2)/totalelements
    return weights



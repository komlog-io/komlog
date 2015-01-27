'''
This file aims to group all variable related methods and data structures

author: jcazor@komlog.org 
date: 2013/03/09
'''
import re
import zlib
import json
from decimal import *

FLOAT_REGEXP='[-+]?[0-9]*[\.,]?[0-9]+'
VAR_SEPARATORS=(' ',';','\n','\t')
VAR_SUFIX=('%')

class Variable:
    def __init__(self, start=None,length=None,content=None,fromdict=None):
        if fromdict:
            self.s=fromdict['s']
            self.l=fromdict['l']
            self.c=fromdict['c']
            self.h=fromdict['h']
            self.md=fromdict['md']
        else:
            self.s=start
            self.l=length
            self.c=content
            self.h={}
            self.md=0

    def sethash(self,offset,length,left_hash, right_hash):
        self.h['l'+str(offset)+':'+str(length)]=left_hash
        self.h['r'+str(offset)+':'+str(length)]=right_hash

    def __eq__(self, other):
        mykeys=list(self.h.keys())
        yourkeys=list(other.h.keys())
        common=list(set(mykeys)&set(yourkeys))
        try:
            for key in common:
                if not self.h[key]==other.h[key]:
                    return False
        except KeyError:
            return False
        return True

    def __repr__(self):
        return "{'s':"+str(self.s)+", 'c':"+self.c+", 'h': "+str(self.h)+"}"

def get_varlist(content=None,jsoncontent=None,onlyvar=None):
    varlist=[]
    if content:
        templist=[]
        p=re.compile(FLOAT_REGEXP)
        for m in p.finditer(content):
            templist.append(m)
        for var in templist:
            try:
                if (content[var.start()-1] in VAR_SEPARATORS) and (content[var.start()+len(var.group())] in VAR_SEPARATORS):
                    varlist.append(Variable(start=var.start(),length=len(var.group()), content=var.group()))
                elif (content[var.start()-1] in VAR_SEPARATORS) and (content[var.start()+len(var.group())] in VAR_SUFIX):
                    varlist.append(Variable(start=var.start(),length=len(var.group()), content=var.group()))
            except IndexError:
                # out of bounds.... mmm store it:
                varlist.append(Variable(start=var.start(),length=len(var.group()), content=var.group()))
        calculate_varmap(varlist,content)
        return varlist
    else:
        for vardict in json.loads(jsoncontent):
            var=Variable(fromdict=vardict)
            if not onlyvar:
                varlist.append(var)
            elif str(onlyvar) == str(var.s):
                varlist.append(var)
                return varlist
        return varlist


def calculate_varmap(varlist,content):
    offset=0
    to_increase_depth=list(range(len(varlist)))
    while len(to_increase_depth)>0:
        for i in to_increase_depth:
            left_string=get_string(offset=offset,start=varlist[i].s,content=content,before=True)
            right_string=get_string(offset=offset,start=varlist[i].s+varlist[i].l-1,content=content,before=False)
            left_hash=zlib.adler32(bytes(left_string,'utf-8'),0xffffffff)
            right_hash=zlib.adler32(bytes(right_string,'utf-8'),0xffffffff)
            varlist[i].sethash(offset,5,left_hash,right_hash)
        offset+=10
        to_increase_depth=[]
        for i,var_1 in enumerate(varlist):
            for j,var_2 in enumerate(varlist):
                if i != j:
                    if var_1==var_2:
                        to_increase_depth.append(i)
                        break
        to_increase_depth=list(set(to_increase_depth))

def get_string(offset,start,content,before):
    string=['' for i in range(5)]
    clean=False
    if before:
        start-=offset
        start-=1
        length=5
        while start>=0 and length>0:
            c=content[start]
            if c in ('0','1','2','3','4','5','6','7','8','9'):
                clean=True
                start-=1
            elif (c in (',','.')) or (content[start+1] in ('0','1','2','3','4','5','6','7','8','9')):
                clean=True
                start-=1
            elif (c == ' ') and (content[start+1] == ' ') and not clean:
                clean=False
                start-=1
            else:
                start-=1
                length-=1
                clean=False
                string[length]=c
    else:
        start+=1
        start+=offset
        length=5
        pos=0
        while pos<length and start<len(content):
            c=content[start]
            if c in ('0','1','2','3','4','5','6','7','8','9'):
                clean=True
                start+=1
            elif (c in (',','.')) and (content[start-1] in ('0','1','2','3','4','5','6','7','8','9')):
                clean=True
                start+=1
            elif (c == ' ') and (content[start-1] == ' ') and not clean:
                clean=False
                start+=1
            else:
                start+=1
                string[pos]=c
                clean=False
                pos+=1
    return ''.join(string)

def get_numericvalueandseparator(old_decsep,varlist,var):
    '''
    This function return the numeric value (float) of a datasource var.
    If the value contains a separator (, or .) the decimal separator will be guessed 
    searching in the complete datasource varlist, so vars added recently has more work to do
    '''
    
    def getdecimal(strnumber,separator):
        millar=',' if separator=='.' else '.'
        try:
            regex=re.compile('.*['+separator+'].*')
            if not regex.match(strnumber):
                '''Only integer part'''
                integer=strnumber
                decimal='0'
            else:
                integer,decimal=strnumber.split(separator)
        except ValueError:
            '''More than one ocurrence of the separator'''
            return False
        else:
            regex=re.compile('.*['+millar+'].*')
            if regex.match(decimal):
                return False
            if regex.match(integer):
                '''It has millar separator'''
                index=0
                newinteger=''
                for value in integer.split(millar):
                    if not index==0 and not len(value)==3:
                        return False
                    else:
                        index+=1
                        newinteger+=value
                integer=newinteger
            number=integer+'.'+decimal
            return Decimal(number)

    regex=re.compile('.*[,.].*')
    m=regex.match(var.c)
    if not m:
        ''' No decimal part'''
        return Decimal(var.c),False
    decsep=old_decsep
    if decsep:
        ''' Decimal separator already established'''
        return getdecimal(var.c,decsep),decsep
    dotfloat=getdecimal(var.c,'.')
    commafloat=getdecimal(var.c,',')
    if dotfloat and commafloat:
        ''' Both decimal separators seems correct, guess over other vars '''
        posdot=0
        poscomma=0
        for var in varlist:
            commavalue=getdecimal(var.c,',')
            dotvalue=getdecimal(var.c,'.')
            if commavalue and dotvalue:
                continue
            elif commavalue:
                poscomma+=1
            elif dotvalue:
                posdot+=1
        if posdot>poscomma:
            return dotfloat,'.'
        elif poscomma>posdot:
            return commafloat,','
        else:
            ''' Bad Luck '''
            return Decimal(-1),False
    elif commafloat:
        ''' decimal separator: , '''
        return commafloat,','
    elif dotfloat:
        ''' decimal separator: . '''
        return dotfloat,'.'
    else:
        ''' WTF '''
        return Decimal(-1),False



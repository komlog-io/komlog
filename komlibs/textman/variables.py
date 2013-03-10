'''
This file aims to group all variable related methods and data structures

author: jcazor@komlog.org 
date: 2013/03/09
'''
import re
import json

FLOAT_REGEXP=u'[-+]?[0-9]*[\.,]?[0-9]+'
VAR_SEPARATORS=(u' ',u';',u'\n',u'\t')
VAR_SUFIX=(u'%')

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
        mykeys=self.h.keys()
        yourkeys=other.h.keys()
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
            elif onlyvar == str(var.s):
                varlist.append(var)
                return varlist
        return varlist


def calculate_varmap(varlist,content):
    offset=0
    to_increase_depth=range(len(varlist))
    while len(to_increase_depth)>0:
        for i in to_increase_depth:
            left_string=get_string(offset=offset,start=varlist[i].s,content=content,before=True)
            right_string=get_string(offset=offset,start=varlist[i].s+varlist[i].l-1,content=content,before=False)
            left_hash=hash(left_string)
            right_hash=hash(right_string)
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
            if c in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9'):
                clean=True
                start-=1
            elif (c in (u',',u'.')) or (content[start+1] in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9')):
                clean=True
                start-=1
            elif (c == u' ') and (content[start+1] == u' ') and not clean:
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
            if c in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9'):
                clean=True
                start+=1
            elif (c in (u',',u'.')) and (content[start-1] in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9')):
                clean=True
                start+=1
            elif (c == u' ') and (content[start-1] == u' ') and not clean:
                clean=False
                start+=1
            else:
                start+=1
                string[pos]=c
                clean=False
                pos+=1
    return ''.join(string)


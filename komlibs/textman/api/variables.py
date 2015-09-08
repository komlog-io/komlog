'''
This file aims to group all variable related methods and data structures

author: jcazor@komlog.org 
'''
import zlib
from decimal import Decimal
from komlibs.textman.model import variables, patterns
from komfig import logger

DEFAULT_BOF_HASH=1
DEFAULT_EOF_HASH=2
DEFAULT_NUMBER_HASH=3
DEFAULT_SPACES_HASH=4

def get_variables_from_text(text_content):
    string=text_content
    varlist=variables.VariableList()
    separators_detected={
                         variables.DECIMAL_SEPARATOR_COMMA:0,
                         variables.DECIMAL_SEPARATOR_DOT:0,
                         variables.DECIMAL_SEPARATOR_NONE:0,
                         variables.DECIMAL_SEPARATOR_UNKNOWN:0,
                        }
    for i,r_object in enumerate(patterns.VAR_REGEXP_OBJECTS):
        for element in r_object.finditer(string):
            start,end=element.span()
            length=end-start
            content=element.group()
            hash_sequence=get_hash_sequence(content=text_content,left_position=start, right_position=end, sequence_deep=4)
            string=string[:start]+'X'*length+string[end:]
            if i in (0,2,3,4,5,6):
                separators_detected[variables.DECIMAL_SEPARATOR_COMMA]+=1
                varlist.add(variables.Variable(position=start, length=length, content=content, hash_sequence=hash_sequence, sequence_deep=4, decimal_separator=variables.DECIMAL_SEPARATOR_COMMA))
            elif i in (1,7,8,9,10,11):
                separators_detected[variables.DECIMAL_SEPARATOR_DOT]+=1
                varlist.add(variables.Variable(position=start, length=length, content=content, hash_sequence=hash_sequence, sequence_deep=4, decimal_separator=variables.DECIMAL_SEPARATOR_DOT))
            elif i==12:
                separators_detected[variables.DECIMAL_SEPARATOR_UNKNOWN]+=1
                varlist.add(variables.Variable(position=start, length=length, content=content, hash_sequence=hash_sequence, sequence_deep=4, decimal_separator=variables.DECIMAL_SEPARATOR_UNKNOWN))
            elif i==13:
                separators_detected[variables.DECIMAL_SEPARATOR_NONE]+=1
                varlist.add(variables.Variable(position=start, length=length, content=content, hash_sequence=hash_sequence, sequence_deep=4, decimal_separator=variables.DECIMAL_SEPARATOR_NONE))
            elif i==14:
                separators_detected[variables.DECIMAL_SEPARATOR_DOT]+=1
                varlist.add(variables.Variable(position=start, length=length, content=content, hash_sequence=hash_sequence, sequence_deep=4, decimal_separator=variables.DECIMAL_SEPARATOR_DOT))
    if separators_detected[variables.DECIMAL_SEPARATOR_UNKNOWN]>0:
        guessed_separator=variables.DECIMAL_SEPARATOR_COMMA if separators_detected[variables.DECIMAL_SEPARATOR_COMMA]>separators_detected[variables.DECIMAL_SEPARATOR_DOT] else variables.DECIMAL_SEPARATOR_DOT
        for variable in varlist:
            if variable.decimal_separator==variables.DECIMAL_SEPARATOR_UNKNOWN:
                variable.decimal_separator=guessed_separator
    recalc_flag=True
    while recalc_flag:
        ambiguous_vars=get_ambiguous_variables(varlist)
        if len(ambiguous_vars)==0:
            recalc_flag=False
        for variable in ambiguous_vars:
            hash_sequence=get_hash_sequence(content=text_content,left_position=variable.position, right_position=variable.position+variable.length, sequence_deep=variable.sequence_deep*2)
            variable.hash_sequence=hash_sequence
            variable.sequence_deep=variable.sequence_deep*2
            varlist.add(variable=variable)
    return varlist

def get_variables_from_serialized_list(serialization):
    variable_list=variables.VariableList(serialization=serialization)
    return variable_list

def get_variable_from_serialized_list(serialization, position):
    variable_list=variables.VariableList(serialization=serialization)
    for variable in variable_list:
        if variable.position==position:
            return variable
    return None

def get_ambiguous_variables(variable_list):
    ambiguous=set()
    for i,var_a in enumerate(variable_list):
        for j,var_b in enumerate(variable_list):
            if i!=j and var_a.hash_sequence==var_b.hash_sequence:
                ambiguous.add(var_a)
                ambiguous.add(var_b)
    return variables.VariableList(variables=list(ambiguous))

def get_hash_sequence(content, left_position, right_position, sequence_deep):
    items_found=0
    sequence={}
    if len(content)>right_position:
        for i,item in enumerate(patterns.ro_hash.finditer(content[right_position:])):
            key='r_'+str(i+1)
            if patterns.ro_number.search(item.group()) and patterns.ro_number.search(item.group()).group()==item.group():
                value=DEFAULT_NUMBER_HASH
            elif patterns.ro_spaces.search(item.group()) and patterns.ro_spaces.search(item.group()).group()==item.group():
                value=DEFAULT_SPACES_HASH
            else:
                value=zlib.adler32(bytes(item.group(),'utf-8'),0xffffffff)
            sequence[key]=value
            items_found+=1
            if items_found==sequence_deep:
                break
    if items_found<sequence_deep:
        key='r_'+str(items_found+1)
        value=DEFAULT_EOF_HASH
        sequence[key]=value
    items_found=0
    if left_position>=1:
        for i,item in enumerate(patterns.ro_hash.finditer(content[left_position-1::-1])):
            key='l_'+str(i+1)
            if patterns.ro_number.search(item.group()) and patterns.ro_number.search(item.group()).group()==item.group():
                value=DEFAULT_NUMBER_HASH
            elif patterns.ro_spaces.search(item.group()) and patterns.ro_spaces.search(item.group()).group()==item.group():
                value=DEFAULT_SPACES_HASH
            else:
                value=zlib.adler32(bytes(item.group(),'utf-8'),0xffffffff)
            sequence[key]=value
            items_found+=1
            if items_found==sequence_deep:
                break
    if items_found<sequence_deep:
        key='l_'+str(items_found+1)
        value=DEFAULT_BOF_HASH
        sequence[key]=value
    return sequence

def get_numeric_value(variable):
    if variable.decimal_separator==variables.DECIMAL_SEPARATOR_NONE:
        numeric_value=variable.content.replace('.','').replace(',','')
        return Decimal(variable.content)
    elif variable.decimal_separator==variables.DECIMAL_SEPARATOR_COMMA:
        numeric_value=variable.content.replace('.','').replace(',','.')
        return Decimal(numeric_value)
    elif variable.decimal_separator==variables.DECIMAL_SEPARATOR_DOT:
        numeric_value=variable.content.replace(',','')
        return Decimal(numeric_value)
    else:
        #wtf
        numeric_value=variable.content.replace('.','').replace(',','')
        return Decimal(numeric_value)


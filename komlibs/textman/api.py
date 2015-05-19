'''
This file aims to group all variable related methods and data structures

author: jcazor@komlog.org 
'''
import re
import zlib
from decimal import Decimal
from komlibs.textman.model import variables
from komfig import logger

VAR_PREFIX_SEPARATOR_REGEXP='(?<=[ \n\t/\|\(\[;:%$#"=])'
VAR_SUFIX_SEPARATOR_REGEXP ='(?=[ \n\t/\|\)\];:%$#"])'
VAR_PREFIX_SEPARATOR_WITH_COMMA_REGEXP='(?<=[, \n\t/\|\(\[;:%$#"=])'
VAR_SUFIX_SEPARATOR_WITH_COMMA_REGEXP='(?=[, \n\t/\|\(\];:%$#"])'

SEPARATOR_REGEXP='([ ]+|[\n\t/\|\(\)\[\];:\.%\$\#"=])'
WORD_REGEXP='([A-Za-z0-9_/]+)'
NUMBER_REGEXP='([0-9]+)'
SPACES_REGEXP='([ ]+)'
ANYTHING_REGEXP='(.{1})'

FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA='([-+]?[0-9]{1,3}(\.[0-9][0-9][0-9])+[,][0-9]+)'
FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT='([-+]?[0-9]{1,3}(,[0-9][0-9][0-9])+[\.][0-9]+)'
FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA='([-+]?[0-9]{4,}[,][0-9]+)'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA='([-+]?[0-9]{0,3}[,][0-9]{4,})'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA='([-+]?[0-9]{0,3}[,][0-9]{1,2})'
FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA='([-+]?[,][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA='([-+]?[0][,][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT='([-+]?[0-9]{4,}[\.][0-9]+)'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT='([-+]?[0-9]{0,3}[\.][0-9]{4,})'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT='([-+]?[0-9]{0,3}[\.][0-9]{1,2})'
FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT='([-+]?[\.][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT='([-+]?[0][\.][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP='([-+]?[0-9]{1,3}[\.,][0-9]{3})'
INTEGER_LEFT_TO_RIGHT='([-+]?[0-9]+)'
FLOAT_LEFT_TO_RIGHT_CSV_FORMATTED='('+VAR_PREFIX_SEPARATOR_WITH_COMMA_REGEXP+'[-+]?[0-9]*[\.]?[0-9]+'+VAR_SUFIX_SEPARATOR_WITH_COMMA_REGEXP+'|^[-+]?[0-9]*[\.]?[0-9]+'+VAR_SUFIX_SEPARATOR_WITH_COMMA_REGEXP+'|'+VAR_PREFIX_SEPARATOR_WITH_COMMA_REGEXP+'[-+]?[0-9]*[\.]?[0-9]+$)'

DEFAULT_BOF_HASH=1
DEFAULT_EOF_HASH=2
DEFAULT_NUMBER_HASH=3
DEFAULT_SPACES_HASH=4

#we have create regex like this because variable-width look-aheads and look-behinds are not supported

ro_var_regex_0=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA+'$')

ro_var_regex_1=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT+'$')

ro_var_regex_2=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA+'$')

ro_var_regex_3=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA+'$')

ro_var_regex_4=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA+'$')

ro_var_regex_5=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA+'$')

ro_var_regex_6=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA+'$')

ro_var_regex_7=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT+'$')

ro_var_regex_8=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT+'$')

ro_var_regex_9=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT+'$')

ro_var_regex_10=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT+'$')

ro_var_regex_11=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT+'$')

ro_var_regex_12=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP+'$') #the can match values like 0,232 o 0.432, check the 0_VALUE regex before this, so we dont have to complicate the expression of this one

ro_var_regex_13=re.compile(VAR_PREFIX_SEPARATOR_REGEXP+INTEGER_LEFT_TO_RIGHT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+INTEGER_LEFT_TO_RIGHT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+INTEGER_LEFT_TO_RIGHT+'$')

ro_var_regex_14=re.compile(FLOAT_LEFT_TO_RIGHT_CSV_FORMATTED)

ro_hash=re.compile(SEPARATOR_REGEXP+'|'+WORD_REGEXP+'|'+NUMBER_REGEXP+'|'+ANYTHING_REGEXP)
ro_number=re.compile(NUMBER_REGEXP)
ro_spaces=re.compile(SPACES_REGEXP)

VAR_REGEXP_OBJECTS=[ro_var_regex_0,
                    ro_var_regex_1,
                    ro_var_regex_2,
                    ro_var_regex_3,
                    ro_var_regex_4,
                    ro_var_regex_5,
                    ro_var_regex_6,
                    ro_var_regex_7,
                    ro_var_regex_8,
                    ro_var_regex_9,
                    ro_var_regex_10,
                    ro_var_regex_11,
                    ro_var_regex_12,
                    ro_var_regex_13,
                    ro_var_regex_14,
                   ]


def get_variables_from_text(text_content):
    string=text_content
    varlist=variables.VariableList()
    separators_detected={
                         variables.DECIMAL_SEPARATOR_COMMA:0,
                         variables.DECIMAL_SEPARATOR_DOT:0,
                         variables.DECIMAL_SEPARATOR_NONE:0,
                         variables.DECIMAL_SEPARATOR_UNKNOWN:0,
                        }
    for i,r_object in enumerate(VAR_REGEXP_OBJECTS):
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
        for i,item in enumerate(ro_hash.finditer(content[right_position:])):
            key='r_'+str(i+1)
            if ro_number.search(item.group()) and ro_number.search(item.group()).group()==item.group():
                value=DEFAULT_NUMBER_HASH
            elif ro_spaces.search(item.group()) and ro_spaces.search(item.group()).group()==item.group():
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
        for i,item in enumerate(ro_hash.finditer(content[left_position-1::-1])):
            key='l_'+str(i+1)
            if ro_number.search(item.group()) and ro_number.search(item.group()).group()==item.group():
                value=DEFAULT_NUMBER_HASH
            elif ro_spaces.search(item.group()) and ro_spaces.search(item.group()).group()==item.group():
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


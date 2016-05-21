'''
This file aims to group all variable related methods and data structures

author: jcazor@komlog.org 
'''

import zlib
from decimal import Decimal
from komlog.komlibs.textman.model import variables, patterns
from komlog.komfig import logging

def get_variables_index_from_text(text):
    string=text
    varindex={}
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
            varindex[start]=length
            string=string[:start]+'X'*length+string[end:]
    return varindex

def get_numeric_value(variable):
    decsep=variable['decsep']
    if decsep==variables.DECIMAL_SEPARATOR_NONE:
        numeric_value=variable['content'].replace('.','').replace(',','')
        return Decimal(numeric_value)
    elif decsep==variables.DECIMAL_SEPARATOR_COMMA:
        numeric_value=variable['content'].replace('.','').replace(',','.')
        return Decimal(numeric_value)
    elif decsep==variables.DECIMAL_SEPARATOR_DOT:
        numeric_value=variable['content'].replace(',','')
        return Decimal(numeric_value)
    else:
        #wtf
        numeric_value=variable['content'].replace('.','').replace(',','')
        return Decimal(numeric_value)

def get_hashed_text(text):
    ''' 
    This function process a text to extract the hashed elements of it.
    The text is decomposed in elements (words, variables, separatos, etc) depending on some
    regular expressions, and returns a list of hashed values, each one corresponding to one
    of those elements. Each element in the list, has also some attributes like the position
    in the text, the position in the line, the line where it is contained, etc.
    '''
    hashlist={'elements':[],'header_lines':[]}
    text_length=len(text)
    if text_length==0:
        return hashlist
    separators_detected={
         variables.DECIMAL_SEPARATOR_COMMA:0,
         variables.DECIMAL_SEPARATOR_DOT:0,
         variables.DECIMAL_SEPARATOR_NONE:0,
         variables.DECIMAL_SEPARATOR_UNKNOWN:0,
    }
    hashed_intervals=[(text_length,text_length)]
    elements=[]
    string=text
    for i,r_object in enumerate(patterns.VAR_REGEXP_OBJECTS):
        for element in r_object.finditer(string):
            start,end=element.span()
            length=end-start
            content=element.group()
            string=string[:start]+'X'*length+string[end:]
            if i in (0,2,3,4,5,6):
                separators_detected[variables.DECIMAL_SEPARATOR_COMMA]+=1
                decimal_separator=variables.DECIMAL_SEPARATOR_COMMA
            elif i in (1,7,8,9,10,11):
                separators_detected[variables.DECIMAL_SEPARATOR_DOT]+=1
                decimal_separator=variables.DECIMAL_SEPARATOR_DOT
            elif i==12:
                separators_detected[variables.DECIMAL_SEPARATOR_UNKNOWN]+=1
                decimal_separator=variables.DECIMAL_SEPARATOR_UNKNOWN
            elif i==13:
                separators_detected[variables.DECIMAL_SEPARATOR_NONE]+=1
                decimal_separator=variables.DECIMAL_SEPARATOR_NONE
            elif i==14:
                separators_detected[variables.DECIMAL_SEPARATOR_DOT]+=1
                decimal_separator=variables.DECIMAL_SEPARATOR_DOT
            elements.append({
                'type':'var',
                'text_pos':start,
                'content':content,
                'length':length,
                'hash':variables.DEFAULT_NUMBER_HASH,
                'decsep':decimal_separator
            })
            hashed_intervals.append((start,end))
    if separators_detected[variables.DECIMAL_SEPARATOR_UNKNOWN]>0:
        guessed_separator=variables.DECIMAL_SEPARATOR_COMMA if separators_detected[variables.DECIMAL_SEPARATOR_COMMA]>separators_detected[variables.DECIMAL_SEPARATOR_DOT] else variables.DECIMAL_SEPARATOR_DOT
        for variable in elements:
            if variable['decsep']==variables.DECIMAL_SEPARATOR_UNKNOWN:
                variable['decsep']=guessed_separator
    interval_init=0
    for interval in sorted(hashed_intervals, key=lambda x:x[0]):
        if interval[0]>interval_init:
            substring=text[interval_init:interval[0]]
            for element in patterns.ro_hash.finditer(substring):
                start,end=element.span()
                length=end-start
                content=element.group()
                if patterns.ro_spaces.search(content) and patterns.ro_spaces.search(content).group()==content:
                    hash_value=variables.DEFAULT_SPACES_HASH
                elif patterns.ro_newline.search(content) and patterns.ro_newline.search(content).group()==content:
                    hash_value=variables.DEFAULT_NEWLINE_HASH
                else:
                    hash_value=zlib.adler32(bytes(element.group(),'utf-8'),0xffffffff)
                text_pos = start+interval_init
                elements.append({
                    'text_pos':text_pos,
                    'length':length,
                    'hash':hash_value,
                })
        interval_init=interval[1]
    sorted_list=sorted(elements, key=lambda x:x['text_pos'])
    line=1
    line_ends={0:0}
    for i,element in enumerate(sorted_list):
        element['order']=i+1
        element['line']=line
        element['line_pos']=element['text_pos']-line_ends[line-1]
        line_ends[line]=element['text_pos']+element['length']
        if element['hash']==variables.DEFAULT_NEWLINE_HASH:
            line+=1
    header_lines=[]
    for lineno in line_ends.keys():
        header_line=True
        num_elements=0
        for element in sorted_list:
            if element['line']==lineno:
                num_elements+=1
                if 'type' in element and element['type']=='var':
                    header_line=False
                    break
            elif element['line']>lineno:
                break
        if header_line and num_elements>0:
            header_lines.append(lineno)
    hashlist['elements']=sorted_list
    hashlist['header_lines']=sorted(header_lines)
    return hashlist

def get_variable_atts(text_hash, text_pos, relative_deep=20, same_line_atts=True, up_col_atts=True, down_col_atts=True, numeric_atts=True):
    var_atts={}
    var = None
    text_elements=sorted(text_hash['elements'], key=lambda x:x['order'])
    for element in text_elements:
        if element['text_pos']<text_pos:
            continue
        elif element['text_pos']==text_pos:
            var=element
            break
        else:
            break
    if not var:
        return {}
    same_line_elements=[]
    up_col_header_element=None
    down_col_header_element=None
    relative_left_elements=[]
    relative_right_elements=[]
    if same_line_atts:
        var_line=var['line']
        var_order=var['order']
        for element in text_elements:
            if element['line']<var_line:
                continue
            elif element['line']==var_line:
                same_line_elements.append(element)
            else:
                break
        last_line_order=0
        last_line_att = variables.LINE+'_'
        for element in same_line_elements:
            if element['order']-var['order']!=0:
                last_line_order = element['order'] if element['order']>last_line_order else last_line_order
                att=variables.LINE+'_'+str(element['order']-var['order'])
                last_line_att=att if last_line_order == element['order'] else last_line_att
                var_atts[att]=element['hash']
                if numeric_atts and 'type' in element and element['type']=='var':
                    att=variables.NUMERIC+'_'+str(element['order']-var['order'])
                    var_atts[att]=element['content']
        if last_line_att in var_atts and var_atts[last_line_att]!=variables.DEFAULT_NEWLINE_HASH:
            att=variables.LINE+'_'+str((last_line_order+1)-var['order'])
            var_atts[att]=variables.DEFAULT_NEWLINE_HASH
    if relative_deep>0:
        var_order=var['order']
        for element in text_elements:
            if element['order']<var_order-relative_deep:
                continue
            elif var_order-relative_deep<=element['order'] and element['order']<=var_order+relative_deep and element['order']!=var['order']:
                att=variables.RELATIVE+'_'+str(element['order']-var['order'])
                var_atts[att]=element['hash']
            else:
                break
        if var_order-relative_deep < 0:
            att=variables.RELATIVE+'_-'+str(var_order)
            var_atts[att]=variables.DEFAULT_BOF_HASH
        if var_order+relative_deep > text_elements[-1]['order']:
            att=variables.RELATIVE+'_'+str(text_elements[-1]['order']-var_order+1)
            var_atts[att]=variables.DEFAULT_EOF_HASH
    if up_col_atts:
        if not len(text_hash['header_lines'])>0:
            att=variables.COLUMN+'_-1'
            var_atts[att]=0
        else:
            var_line=var['line']
            var_line_pos=var['line_pos']
            up_line=None
            up_element=None
            for line in text_hash['header_lines']:
                if line<var_line:
                    up_line=line
                else:
                    break
            if not up_line:
                att=variables.COLUMN+'_-1'
                var_atts[att]=0
            else:
                for element in text_elements:
                    if element['line']<up_line:
                        continue
                    elif element['line']==up_line and element['line_pos']+element['length']>var['line_pos']:
                        up_element=element
                        break
                    elif element['line']>up_line:
                        break
                if up_element:
                    att=variables.COLUMN+'_-1'
                    var_atts[att]=up_element['hash']
    if down_col_atts:
        if not len(text_hash['header_lines'])>0:
            att=variables.COLUMN+'_1'
            var_atts[att]=0
        else:
            var_line=var['line']
            var_line_pos=var['line_pos']
            down_line=None
            down_element=None
            for line in text_hash['header_lines'][::-1]:
                if line>var_line:
                    down_line=line
                else:
                    break
            if not down_line:
                att=variables.COLUMN+'_1'
                var_atts[att]=0
            else:
                for element in text_elements:
                    if element['line']<down_line:
                        continue
                    elif element['line']==down_line and element['line_pos']+element['length']>var['line_pos']:
                        down_element=element
                        break
                    elif element['line']>down_line:
                        break
                if down_element:
                    att=variables.COLUMN+'_1'
                    var_atts[att]=down_element['hash']
    return var_atts

def get_variables_atts(text_hash):
    variables_atts=[]
    variables_list=[]
    for element in text_hash['elements']:
        if 'type' in element and element['type']=='var':
            variables_list.append(element)
    for var in variables_list:
        var_atts=get_variable_atts(text_hash=text_hash, text_pos=var['text_pos'])
        variables_atts.append({'text_pos':var['text_pos'],'atts':var_atts})
    return variables_atts


'''
This file defines the different data structures that the text manipulation module manages

author: jcazor@komlog.org 
date: 2015/03/26
'''

import json

DECIMAL_SEPARATOR_COMMA=','
DECIMAL_SEPARATOR_DOT='.'
DECIMAL_SEPARATOR_NONE='n'
DECIMAL_SEPARATOR_UNKNOWN='u'

class Variable:
    def __init__(self, position=0, length=0, content='', hash_sequence={}, sequence_deep=0, decimal_separator=DECIMAL_SEPARATOR_UNKNOWN, serialization=None):
        if serialization:
            self.content=None
            self._deserialize(serialized_content=serialization)
        else:
            self.position=position
            self.length=length
            self.content=content
            self.hash_sequence=hash_sequence
            self.sequence_deep=sequence_deep
            self.decimal_separator=decimal_separator

    def serialize(self):
        serialization={}
        serialization['p']=self.position
        serialization['c']=self.content
        serialization['l']=self.length
        serialization['h']=self.hash_sequence
        serialization['sd']=self.sequence_deep
        serialization['dc']=self.decimal_separator
        return json.dumps(serialization)

    def _deserialize(self, serialized_content):
        if not self.content is None:
            #do nothing if self.content has been initialized previously
            return
        serialized_dict=json.loads(serialized_content)
        for key in ['p','c','l','h','sd','dc']:
            if key not in serialized_dict:
                #incomplete serialization
                return
        self.position=serialized_dict['p']
        self.length=serialized_dict['l']
        self.content=serialized_dict['c']
        self.hash_sequence=serialized_dict['h']
        self.sequence_deep=serialized_dict['sd']
        self.decimal_separator=serialized_dict['dc']

class VariableList:
    def __init__(self, variables=None, serialization=None):
        if serialization:
            self.variables=None
            self._deserialize(serialized_content=serialization)
        else:
            self.variables=variables if variables else []

    def serialize(self):
        serialized_variables=[]
        for var in self.variables:
            serialized_variables.append(var.serialize())
        return json.dumps(serialized_variables)
    
    def _deserialize(self, serialized_content):
        if not self.variables is None:
            #do nothing if self.variables has been populated previously
            return
        self.variables=[]
        serialized_list=json.loads(serialized_content)
        for serialized_variable in serialized_list:
            var=Variable(serialization=serialized_variable)
            self.variables.append(var)

    def get_index(self):
        index={}
        for var in self.variables:
            index[var.position]=var.length
        return index

    def add(self, variable):
        for var in self.variables:
            if var.position==variable.position:
                self.variables.remove(var)
        self.variables.append(variable)

    def __iter__(self):
        for var in self.variables:
            yield var

    def __len__(self):
        return len(self.variables)


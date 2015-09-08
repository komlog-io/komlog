import unittest
import uuid
from decimal import Decimal
from komlibs.textman.api import variables as varapi
from komlibs.textman.model import variables as varmodel
from komfig import logger

class TextmanApiVariablesTest(unittest.TestCase):
    ''' komlibs.textman.api.variables tests '''

    def test_get_variables_from_text_success_text_with_decimal_separator_comma(self):
        ''' get_variables_from_text should return a VariableList object, with de Variable objects, each one representing a variable found. The Variable objects should have the position in the text, lenght of the variable found, content, decimal separator and hash sequence '''
        text='vars: 1.111.111,1  1111,1 11,1111 0,111 1,1 1,111 '
        variablelist=varapi.get_variables_from_text(text_content=text)
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==6:
                self.assertEqual(variable.length,11)
                self.assertEqual(variable.content,'1.111.111,1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==19:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111,1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==26:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11,1111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==34:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0,111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==40:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1,1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==44:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'1,111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variables_from_text_success_text_with_decimal_separator_dot(self):
        ''' get_variables_from_text should return a VariableList object, with de Variable objects, each one representing a variable found. The Variable objects should have the position in the text, lenght of the variable found, content, decimal separator and hash sequence '''
        text='vars: 1,111,111.1  1111.1 11.1111 0.111 1.1 1.111 '
        variablelist=varapi.get_variables_from_text(text_content=text)
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==6:
                self.assertEqual(variable.length,11)
                self.assertEqual(variable.content,'1,111,111.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==19:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==26:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11.1111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==34:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0.111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==40:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==44:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'1.111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variables_from_text_success_text_with_csv_format(self):
        ''' get_variables_from_text should return a VariableList object, with de Variable objects, each one representing a variable found. The Variable objects should have the position in the text, lenght of the variable found, content, decimal separator and hash sequence '''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        variablelist=varapi.get_variables_from_text(text_content=text)
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==0:
                self.assertEqual(variable.length,9)
                self.assertEqual(variable.content,'1111111.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==10:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==17:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11.1111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==25:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0.111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==31:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==35:
                self.assertEqual(variable.length,1)
                self.assertEqual(variable.content,'1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variables_from_serialized_list(self):
        ''' get_variables_from_serialized_list should return a VariableList object with the Variables '''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        variablelist_orig=varapi.get_variables_from_text(text_content=text)
        serialized_list=variablelist_orig.serialize()
        self.assertTrue(isinstance(serialized_list, str))
        variablelist=varapi.get_variables_from_serialized_list(serialized_list)
        self.assertTrue(isinstance(variablelist,varmodel.VariableList))
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==0:
                self.assertEqual(variable.length,9)
                self.assertEqual(variable.content,'1111111.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==10:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==17:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11.1111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==25:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0.111')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==31:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1.1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==35:
                self.assertEqual(variable.length,1)
                self.assertEqual(variable.content,'1')
                self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variable_from_serialized_list(self):
        ''' get_variable_from_serialized_list should return the Variable object in the indicated position '''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        variablelist_orig=varapi.get_variables_from_text(text_content=text)
        serialized_list=variablelist_orig.serialize()
        self.assertTrue(isinstance(serialized_list, str))
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=0)
        self.assertEqual(variable.position,0)
        self.assertEqual(variable.length,9)
        self.assertEqual(variable.content,'1111111.1')
        self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=10)
        self.assertEqual(variable.position,10)
        self.assertEqual(variable.length,6)
        self.assertEqual(variable.content,'1111.1')
        self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=17)
        self.assertEqual(variable.position,17)
        self.assertEqual(variable.length,7)
        self.assertEqual(variable.content,'11.1111')
        self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=25)
        self.assertEqual(variable.position,25)
        self.assertEqual(variable.length,5)
        self.assertEqual(variable.content,'0.111')
        self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=31)
        self.assertEqual(variable.position,31)
        self.assertEqual(variable.length,3)
        self.assertEqual(variable.content,'1.1')
        self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=35)
        self.assertEqual(variable.position,35)
        self.assertEqual(variable.length,1)
        self.assertEqual(variable.content,'1')
        self.assertEqual(variable.decimal_separator,varmodel.DECIMAL_SEPARATOR_DOT)
        variable=varapi.get_variable_from_serialized_list(serialization=serialized_list, position=323)
        self.assertIsNone(variable)

    def test_get_variable_from_serialized_list(self):
        ''' get_numeric_value should return a Decimal with the numeric value of the variable '''
        variable=varmodel.Variable(content='1',decimal_separator=varmodel.DECIMAL_SEPARATOR_DOT)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=varmodel.Variable(content='1',decimal_separator=varmodel.DECIMAL_SEPARATOR_COMMA)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=varmodel.Variable(content='1',decimal_separator=varmodel.DECIMAL_SEPARATOR_NONE)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=varmodel.Variable(content='1',decimal_separator=varmodel.DECIMAL_SEPARATOR_UNKNOWN)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=varmodel.Variable(content='1.1',decimal_separator=varmodel.DECIMAL_SEPARATOR_DOT)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1.1'))
        variable=varmodel.Variable(content='1.1',decimal_separator=varmodel.DECIMAL_SEPARATOR_COMMA)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('11'))
        variable=varmodel.Variable(content='1,1',decimal_separator=varmodel.DECIMAL_SEPARATOR_DOT)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('11'))
        variable=varmodel.Variable(content='1,1',decimal_separator=varmodel.DECIMAL_SEPARATOR_COMMA)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1.1'))
        variable=varmodel.Variable(content='1,111,111.11',decimal_separator=varmodel.DECIMAL_SEPARATOR_DOT)
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1111111.11'))


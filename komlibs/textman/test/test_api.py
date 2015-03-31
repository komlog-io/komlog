import unittest
import uuid
from decimal import Decimal
from komlibs.textman import api
from komlibs.textman.model import variables
from komfig import logger

class TextmanApiTest(unittest.TestCase):
    ''' komlibs.textman.api tests '''

    def test_ro_var_regex_0_success(self):
        ''' api.ro_var_regex_0 should detect variables with thousand separators (.) and decimal separator (,) '''
        valids=[';1.000.000,32:  ',
                ' +1.000.000,32% ',
                ' -320.233,45%   ',
                ' 222.222,222222 ',
               ]
        invalids=[' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2,222,222.121  ',
                  ' 2.222.2222,222 ',
                  ' 3,333,333.32   ',
                  ' 2222,32        ',
                  ' 2222.343       ',
                  ' 23434,342      ',
                  ' ,243           ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 1,2323         ',
                  ' 32,32          ',
                  ' 32.13          ',
                  ' 0,232          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_0.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_0.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_1_success(self):
        ''' api.ro_var_regex_1 should detect variables with thousand separators (,) and decimal separator (.) '''
        valids=[';1,000,000.32:  ',
                ' +1,000,000.32% ',
                ' -320,233.45%   ',
                ' 222,222.222222 ',
               ]
        invalids=[' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 2222,32        ',
                  ' 2222.343       ',
                  ' 23434,342      ',
                  ' ,243           ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 1,2323         ',
                  ' 32,32          ',
                  ' 32.13          ',
                  ' 0,232          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_1.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_1.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_2_success(self):
        ''' api.ro_var_regex_2 should detect variables with 4 or more digits in the integer part, without thousand separators, and any number of decimal digits, with decimal separator comma (,) '''
        valids=[
                  ' 2222,32        ',
                  ' 23434,342      ',
               ]
        invalids=[
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 2222.343       ',
                  ' ,243           ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 1,2323         ',
                  ' 32,32          ',
                  ' 32.13          ',
                  ' 0,232          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_2.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_2.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_3_success(self):
        ''' api.ro_var_regex_3 should detect variables with 0 to 3 digits in the integer part, without thousand separators, and 4 or more decimal digits, with decimal separator comma (,) '''
        valids=[
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
               ]
        invalids=[
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 2222.343       ',
                  ' ,243           ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 32,32          ',
                  ' 32.13          ',
                  ' 0,232          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_3.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_3.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_4_success(self):
        ''' api.ro_var_regex_4 should detect variables with 0 to 3 digits in the integer part, without thousand separators, and between 1 and 2 decimal digits, with decimal separator comma (,) '''
        valids=[
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
               ]
        invalids=[
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 2222.343       ',
                  ' ,243           ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 32.13          ',
                  ' 0,232          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_4.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_4.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_5_success(self):
        ''' api.ro_var_regex_5 should detect variables with 0 digits in the integer part, and 3 decimal digits, with decimal separator comma (,) '''
        valids=[
                  ' ,243           ',
               ]
        invalids=[
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 2222.343       ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 32.13          ',
                  ' 0,232          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_5.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_5.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_6_success(self):
        ''' api.ro_var_regex_6 should detect variables with a 0 in the integer part, and 3 decimal digits, with decimal separator comma (,) '''
        valids=[
                  ' 0,232          ',
               ]
        invalids=[
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 2222.343       ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 32.13          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_6.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_6.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_7_success(self):
        ''' api.ro_var_regex_7 should detect variables with 4 or more digits in the integer part, without thousand separators, and any number of decimal digits, with decimal separator dot (.) '''
        valids=[
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
               ]
        invalids=[
                  ' 0,232          ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.2222        ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 32.13          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_7.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_7.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_8_success(self):
        ''' api.ro_var_regex_8 should detect variables with 0 to 3 digits in the integer part, without thousand separators, and 4 or more decimal digits, with decimal separator dot (.) '''
        valids=[
                  ' 22.2222        ',
                  ' 2.2222         ',
                  ' .2222          ',
                  ' 22.222222      ',
                  ' 1.2321         ',
               ]
        invalids=[
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
                  ' 0,232          ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1            ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' .434           ',
                  ' 32.13          ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_8.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_8.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_9_success(self):
        ''' api.ro_var_regex_9 should detect variables with 0 to 3 digits in the integer part, without thousand separators, and between 1 and 2 decimal digits, with decimal separator dot (.) '''
        valids=[
                  ' 1.1            ',
                  ' 1.12           ',
                  ' 32.1           ',
                  ' 32.13          ',
                  ' 321.1          ',
                  ' 321.13         ',
                  ' .1             ',
                  ' .13            ',
               ]
        invalids=[
                  ' 22.2222        ',
                  ' 2.2222         ',
                  ' .2222          ',
                  ' 22.222222      ',
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
                  ' 0,232          ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' .434           ',
                  ' 1.2321         ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_9.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_9.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_10_success(self):
        ''' api.ro_var_regex_10 should detect variables with no integer part and 3 decimal digits, with decimal separator dot (.) '''
        valids=[
                  ' .434           ',
               ]
        invalids=[
                  ' 1.1            ',
                  ' 1.12           ',
                  ' 32.1           ',
                  ' 32.13          ',
                  ' 321.1          ',
                  ' 321.13         ',
                  ' .1             ',
                  ' .13            ',
                  ' 22.2222        ',
                  ' 2.2222         ',
                  ' .2222          ',
                  ' 22.222222      ',
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
                  ' 0,232          ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 1.2321         ',
                  ' 0.232          ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_10.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_10.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_11_success(self):
        ''' api.ro_var_regex_11 should detect variables with a 0 in the integer part, and 3 decimal digits, with decimal separator dot (.) '''
        valids=[
                  ' 0.232          ',
               ]
        invalids=[
                  ' .434           ',
                  ' 1.1            ',
                  ' 1.12           ',
                  ' 32.1           ',
                  ' 32.13          ',
                  ' 321.1          ',
                  ' 321.13         ',
                  ' .1             ',
                  ' .13            ',
                  ' 22.2222        ',
                  ' 2.2222         ',
                  ' .2222          ',
                  ' 22.222222      ',
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
                  ' 0,232          ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 22.222         ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 1.2321         ',
                  ' 12,121         ',
                  ' 12.121         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_11.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_11.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_12_success(self):
        ''' api.ro_var_regex_12 should detect variables with a 1 to 3 digits in the integer part, and 3 decimal digits, with decimal separator dot or comma  (. or ,) '''
        valids=[
                  ' 0.232          ',
                  ' 0,232          ',
                  ' 22.222         ',
                  ' 12,121         ',
                  ' 12.121         ',
               ]
        invalids=[
                  ' .434           ',
                  ' 1.1            ',
                  ' 1.12           ',
                  ' 32.1           ',
                  ' 32.13          ',
                  ' 321.1          ',
                  ' 321.13         ',
                  ' .1             ',
                  ' .13            ',
                  ' 22.2222        ',
                  ' 2.2222         ',
                  ' .2222          ',
                  ' 22.222222      ',
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1              ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 1.2321         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_12.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_12.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_13_success(self):
        ''' api.ro_var_regex_13 should detect variables with only integer part '''
        valids=[
                  ' 1              ',
                  ' 12312          ',
                  ' 0123443        ',
                  ' +142           ',
                  ' -132           ',
               ]
        invalids=[
                  ' 0.232          ',
                  ' 0,232          ',
                  ' 22.222         ',
                  ' 12,121         ',
                  ' 12.121         ',
                  ' .434           ',
                  ' 1.1            ',
                  ' 1.12           ',
                  ' 32.1           ',
                  ' 32.13          ',
                  ' 321.1          ',
                  ' 321.13         ',
                  ' .1             ',
                  ' .13            ',
                  ' 22.2222        ',
                  ' 2.2222         ',
                  ' .2222          ',
                  ' 22.222222      ',
                  ' 2222.343       ',
                  ' 2222.34        ',
                  ' 222222.3       ',
                  ' 2222.343333    ',
                  ' ,243           ',
                  ' 32,32          ',
                  ' 32,3           ',
                  ' ,32            ',
                  ' 2,32           ',
                  ' 2,3            ',
                  ' 1,2323         ',
                  ' 123,2323       ',
                  ' ,2323          ',
                  ' ,23232323      ',
                  ' 2222,32        ',
                  ' 23434,342      ',
                  ';1,000,000.32:  ',
                  ' +1,000,000.32% ',
                  ' -320,233.45%   ',
                  ' 222,222.222222 ',
                  ' 1.1.1          ',
                  ' 1,1,1          ',
                  ' 2.222.222,121  ',
                  ' 2,222,2222.222 ',
                  ' 3.333.333,32   ',
                  ' 1.2321         ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_13.findall(string)
            self.assertEqual(len(items_found),1)
        for string in invalids:
            items_found=api.ro_var_regex_13.findall(string)
            self.assertEqual(items_found,[])

    def test_ro_var_regex_14_success(self):
        ''' api.ro_var_regex_14 should detect variables in CVS format, that is separated with commas and decimal separator dot, this will match almost any number but those inside words or with more than one dot '.' character '''
        valids=[
                  '1,1,1',
                  '1.2,1.43,1.3424',
                  '1.0,+1.342,-1.4',
                  '3241,-231,+1',
               ]
        invalids=[
                  ' 1.1.1          ',
                  ' 2.222.222      ',
                  ' 3.333.333      ',
                ]
        for string in valids:
            items_found=api.ro_var_regex_14.findall(string)
            self.assertEqual(len(items_found),3)
        for string in invalids:
            items_found=api.ro_var_regex_14.findall(string)
            self.assertEqual(items_found,[])

    def test_get_variables_from_text_success_text_with_decimal_separator_comma(self):
        ''' get_variables_from_text should return a VariableList object, with de Variable objects, each one representing a variable found. The Variable objects should have the position in the text, lenght of the variable found, content, decimal separator and hash sequence '''
        text='vars: 1.111.111,1  1111,1 11,1111 0,111 1,1 1,111 '
        variablelist=api.get_variables_from_text(text_content=text)
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==6:
                self.assertEqual(variable.length,11)
                self.assertEqual(variable.content,'1.111.111,1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==19:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111,1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==26:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11,1111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==34:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0,111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==40:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1,1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
            elif variable.position==44:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'1,111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_COMMA)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variables_from_text_success_text_with_decimal_separator_dot(self):
        ''' get_variables_from_text should return a VariableList object, with de Variable objects, each one representing a variable found. The Variable objects should have the position in the text, lenght of the variable found, content, decimal separator and hash sequence '''
        text='vars: 1,111,111.1  1111.1 11.1111 0.111 1.1 1.111 '
        variablelist=api.get_variables_from_text(text_content=text)
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==6:
                self.assertEqual(variable.length,11)
                self.assertEqual(variable.content,'1,111,111.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==19:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==26:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11.1111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==34:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0.111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==40:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==44:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'1.111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variables_from_text_success_text_with_csv_format(self):
        ''' get_variables_from_text should return a VariableList object, with de Variable objects, each one representing a variable found. The Variable objects should have the position in the text, lenght of the variable found, content, decimal separator and hash sequence '''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        variablelist=api.get_variables_from_text(text_content=text)
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==0:
                self.assertEqual(variable.length,9)
                self.assertEqual(variable.content,'1111111.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==10:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==17:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11.1111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==25:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0.111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==31:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==35:
                self.assertEqual(variable.length,1)
                self.assertEqual(variable.content,'1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variables_from_serialized_list(self):
        ''' get_variables_from_serialized_list should return a VariableList object with the Variables '''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        variablelist_orig=api.get_variables_from_text(text_content=text)
        serialized_list=variablelist_orig.serialize()
        self.assertTrue(isinstance(serialized_list, str))
        variablelist=api.get_variables_from_serialized_list(serialized_list)
        self.assertTrue(isinstance(variablelist, variables.VariableList))
        self.assertEqual(len(variablelist),6)
        total_vars=0
        for variable in variablelist:
            if variable.position==0:
                self.assertEqual(variable.length,9)
                self.assertEqual(variable.content,'1111111.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==10:
                self.assertEqual(variable.length,6)
                self.assertEqual(variable.content,'1111.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==17:
                self.assertEqual(variable.length,7)
                self.assertEqual(variable.content,'11.1111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==25:
                self.assertEqual(variable.length,5)
                self.assertEqual(variable.content,'0.111')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==31:
                self.assertEqual(variable.length,3)
                self.assertEqual(variable.content,'1.1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
            elif variable.position==35:
                self.assertEqual(variable.length,1)
                self.assertEqual(variable.content,'1')
                self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
                total_vars+=1
        self.assertEqual(total_vars,6)

    def test_get_variable_from_serialized_list(self):
        ''' get_variable_from_serialized_list should return the Variable object in the indicated position '''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        variablelist_orig=api.get_variables_from_text(text_content=text)
        serialized_list=variablelist_orig.serialize()
        self.assertTrue(isinstance(serialized_list, str))
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=0)
        self.assertEqual(variable.position,0)
        self.assertEqual(variable.length,9)
        self.assertEqual(variable.content,'1111111.1')
        self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=10)
        self.assertEqual(variable.position,10)
        self.assertEqual(variable.length,6)
        self.assertEqual(variable.content,'1111.1')
        self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=17)
        self.assertEqual(variable.position,17)
        self.assertEqual(variable.length,7)
        self.assertEqual(variable.content,'11.1111')
        self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=25)
        self.assertEqual(variable.position,25)
        self.assertEqual(variable.length,5)
        self.assertEqual(variable.content,'0.111')
        self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=31)
        self.assertEqual(variable.position,31)
        self.assertEqual(variable.length,3)
        self.assertEqual(variable.content,'1.1')
        self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=35)
        self.assertEqual(variable.position,35)
        self.assertEqual(variable.length,1)
        self.assertEqual(variable.content,'1')
        self.assertEqual(variable.decimal_separator,variables.DECIMAL_SEPARATOR_DOT)
        variable=api.get_variable_from_serialized_list(serialization=serialized_list, position=323)
        self.assertIsNone(variable)

    def test_get_variable_from_serialized_list(self):
        ''' get_numeric_value should return a Decimal with the numeric value of the variable '''
        variable=variables.Variable(content='1',decimal_separator=variables.DECIMAL_SEPARATOR_DOT)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=variables.Variable(content='1',decimal_separator=variables.DECIMAL_SEPARATOR_COMMA)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=variables.Variable(content='1',decimal_separator=variables.DECIMAL_SEPARATOR_NONE)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=variables.Variable(content='1',decimal_separator=variables.DECIMAL_SEPARATOR_UNKNOWN)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable=variables.Variable(content='1.1',decimal_separator=variables.DECIMAL_SEPARATOR_DOT)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1.1'))
        variable=variables.Variable(content='1.1',decimal_separator=variables.DECIMAL_SEPARATOR_COMMA)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('11'))
        variable=variables.Variable(content='1,1',decimal_separator=variables.DECIMAL_SEPARATOR_DOT)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('11'))
        variable=variables.Variable(content='1,1',decimal_separator=variables.DECIMAL_SEPARATOR_COMMA)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1.1'))
        variable=variables.Variable(content='1,111,111.11',decimal_separator=variables.DECIMAL_SEPARATOR_DOT)
        value=api.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1111111.11'))


import unittest
import uuid
from decimal import Decimal
from komlog.komlibs.textman.api import variables as varapi
from komlog.komlibs.textman.model import variables as varmodel
from komlog.komfig import logging

class TextmanApiVariablesTest(unittest.TestCase):
    ''' komlibs.textman.api.variables tests '''

    def test_get_variables_index_from_text_no_variables(self):
        ''' get_variables_index_from_text should return an empty dict if no variable is found '''
        text='get_variables_index_from_text no variables found'
        self.assertEqual(varapi.get_variables_index_from_text(text), dict())

    def test_get_variables_index_from_text_success_text_with_decimal_separator_comma(self):
        ''' get_variables_index_from_text should return a dictionary with the positions and lengths of the found variables. In this case, the variables have comma as decimal separator '''
        text='vars: 1.111.111,1  1111,1 11,1111 0,111 1,1 1,111 '
        index=varapi.get_variables_index_from_text(text)
        self.assertEqual(len(index.keys()),6)
        self.assertEqual(index[6],11)
        self.assertEqual(index[19],6)
        self.assertEqual(index[26],7)
        self.assertEqual(index[34],5)
        self.assertEqual(index[40],3)
        self.assertEqual(index[44],5)

    def test_get_variables_index_from_text_success_text_with_decimal_separator_dot(self):
        ''' get_variables_index_from_text should return a dictionary with the positions and lengths of the found variables. In this case, the variables have dot as decimal separator '''
        text='vars: 1,111,111.1  1111.1 11.1111 0.111 1.1 1.111 '
        index=varapi.get_variables_index_from_text(text)
        self.assertEqual(len(index.keys()),6)
        self.assertEqual(index[6],11)
        self.assertEqual(index[19],6)
        self.assertEqual(index[26],7)
        self.assertEqual(index[34],5)
        self.assertEqual(index[40],3)
        self.assertEqual(index[44],5)

    def test_get_variables_index_from_text_success_text_with_csv_format(self):
        ''' get_variables_index_from_text should return a dictionary with the positions and lengths of the found variables. In this case, the variables have dot as decimal separator in csv format'''
        text='1111111.1,1111.1,11.1111,0.111,1.1,1'
        index=varapi.get_variables_index_from_text(text)
        self.assertEqual(len(index.keys()),6)
        self.assertEqual(index[0],9)
        self.assertEqual(index[10],6)
        self.assertEqual(index[17],7)
        self.assertEqual(index[25],5)
        self.assertEqual(index[31],3)
        self.assertEqual(index[35],1)

    def test_get_numeric_value_success(self):
        ''' get_numeric_value should return a Decimal with the numeric value of the variable '''
        variable={'content':'1','decsep':varmodel.DECIMAL_SEPARATOR_DOT}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable={'content':'1','decsep':varmodel.DECIMAL_SEPARATOR_COMMA}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable={'content':'1','decsep':varmodel.DECIMAL_SEPARATOR_NONE}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable={'content':'1','decsep':varmodel.DECIMAL_SEPARATOR_UNKNOWN}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1'))
        variable={'content':'1.1','decsep':varmodel.DECIMAL_SEPARATOR_DOT}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1.1'))
        variable={'content':'1.1','decsep':varmodel.DECIMAL_SEPARATOR_COMMA}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('11'))
        variable={'content':'1,1','decsep':varmodel.DECIMAL_SEPARATOR_DOT}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('11'))
        variable={'content':'1,1','decsep':varmodel.DECIMAL_SEPARATOR_COMMA}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1.1'))
        variable={'content':'1,111,111.11','decsep':varmodel.DECIMAL_SEPARATOR_DOT}
        value=varapi.get_numeric_value(variable=variable)
        self.assertEqual(value,Decimal('1111111.11'))

    def test_get_hashed_text_empty_text(self):
        ''' get_hashed_text should return a dict with no elements '''
        text=''
        hashed_text=varapi.get_hashed_text(text)
        self.assertEqual(hashed_text, {'elements':[],'header_lines':[]})

    def test_get_hashed_text(self):
        ''' get_hashed_text should return a dict with the elements and header_lines found '''
        text='S.ficheros     bloques de 1K  Usados Disponibles Uso% Montado en\ndev                  1540336       0     1540336   0% /dev\nrun                  1542888     516     1542372   1% /run\n/dev/sda3            7092728 6019072      690324  90% /\ntmpfs                1542888       0     1542888   0% /dev/shm\ntmpfs                1542888       0     1542888   0% /sys/fs/cgroup\ntmpfs                1542888     532     1542356   1% /tmp\n/dev/sda1             516040   37280      452548   8% /boot\ntmpfs                 308580       0      308580   0% /run/user/1001\ntmpfs                 308580       0      308580   0% /run/user/1000\ntmpfs                 308580       0      308580   0% /run/user/0\n'
        hashed_text={'header_lines': [1], 'elements': [
        {'length': 1, 'hash': 7274593, 'line_pos': 0, 'line': 1, 'text_pos': 0, 'order': 1},
        {'length': 1, 'hash': 4849724, 'line_pos': 1, 'line': 1, 'text_pos': 1, 'order': 2},
        {'length': 8, 'hash': 253887329, 'line_pos': 2, 'line': 1, 'text_pos': 2, 'order': 3},
        {'length': 5, 'hash': 4, 'line_pos': 10, 'line': 1, 'text_pos': 10, 'order': 4},
        {'length': 7, 'hash': 204538633, 'line_pos': 15, 'line': 1, 'text_pos': 15, 'order': 5},
        {'length': 1, 'hash': 4, 'line_pos': 22, 'line': 1, 'text_pos': 22, 'order': 6},
        {'length': 2, 'hash': 22479063, 'line_pos': 23, 'line': 1, 'text_pos': 23, 'order': 7},
        {'length': 1, 'hash': 4, 'line_pos': 25, 'line': 1, 'text_pos': 25, 'order': 8},
        {'length': 2, 'hash': 14090378, 'line_pos': 26, 'line': 1, 'text_pos': 26, 'order': 9},
        {'length': 2, 'hash': 4, 'line_pos': 28, 'line': 1, 'text_pos': 28, 'order': 10},
        {'length': 6, 'hash': 144704125, 'line_pos': 30, 'line': 1, 'text_pos': 30, 'order': 11},
        {'length': 1, 'hash': 4, 'line_pos': 36, 'line': 1, 'text_pos': 36, 'order': 12},
        {'length': 11, 'hash': 451675274, 'line_pos': 37, 'line': 1, 'text_pos': 37, 'order': 13},
        {'length': 1, 'hash': 4, 'line_pos': 48, 'line': 1, 'text_pos': 48, 'order': 14},
        {'length': 3, 'hash': 42729797, 'line_pos': 49, 'line': 1, 'text_pos': 49, 'order': 15},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 1, 'text_pos': 52, 'order': 16},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 1, 'text_pos': 53, 'order': 17},
        {'length': 7, 'hash': 192217824, 'line_pos': 54, 'line': 1, 'text_pos': 54, 'order': 18},
        {'length': 1, 'hash': 4, 'line_pos': 61, 'line': 1, 'text_pos': 61, 'order': 19},
        {'length': 2, 'hash': 23199969, 'line_pos': 62, 'line': 1, 'text_pos': 62, 'order': 20},
        {'length': 1, 'hash': 5, 'line_pos': 64, 'line': 1, 'text_pos': 64, 'order': 21},
        {'length': 3, 'hash': 44302669, 'line_pos': 0, 'line': 2, 'text_pos': 65, 'order': 22},
        {'length': 18, 'hash': 4, 'line_pos': 3, 'line': 2, 'text_pos': 68, 'order': 23},
        {'type': 'var', 'content': '1540336', 'decsep': 'n', 'line_pos': 21, 'hash': 3, 'length': 7, 'line': 2, 'text_pos': 86, 'order': 24},
        {'length': 7, 'hash': 4, 'line_pos': 28, 'line': 2, 'text_pos': 93, 'order': 25},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 35, 'hash': 3, 'length': 1, 'line': 2, 'text_pos': 100, 'order': 26},
        {'length': 5, 'hash': 4, 'line_pos': 36, 'line': 2, 'text_pos': 101, 'order': 27},
        {'type': 'var', 'content': '1540336', 'decsep': 'n', 'line_pos': 41, 'hash': 3, 'length': 7, 'line': 2, 'text_pos': 106, 'order': 28},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 2, 'text_pos': 113, 'order': 29},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 2, 'text_pos': 116, 'order': 30},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 2, 'text_pos': 117, 'order': 31},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 2, 'text_pos': 118, 'order': 32},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 2, 'text_pos': 119, 'order': 33},
        {'length': 3, 'hash': 44302669, 'line_pos': 55, 'line': 2, 'text_pos': 120, 'order': 34},
        {'length': 1, 'hash': 5, 'line_pos': 58, 'line': 2, 'text_pos': 123, 'order': 35},
        {'length': 3, 'hash': 48628067, 'line_pos': 0, 'line': 3, 'text_pos': 124, 'order': 36},
        {'length': 18, 'hash': 4, 'line_pos': 3, 'line': 3, 'text_pos': 127, 'order': 37},
        {'type': 'var', 'content': '1542888', 'decsep': 'n', 'line_pos': 21, 'hash': 3, 'length': 7, 'line': 3, 'text_pos': 145, 'order': 38},
        {'length': 5, 'hash': 4, 'line_pos': 28, 'line': 3, 'text_pos': 152, 'order': 39},
        {'type': 'var', 'content': '516', 'decsep': 'n', 'line_pos': 33, 'hash': 3, 'length': 3, 'line': 3, 'text_pos': 157, 'order': 40},
        {'length': 5, 'hash': 4, 'line_pos': 36, 'line': 3, 'text_pos': 160, 'order': 41},
        {'type': 'var', 'content': '1542372', 'decsep': 'n', 'line_pos': 41, 'hash': 3, 'length': 7, 'line': 3, 'text_pos': 165, 'order': 42},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 3, 'text_pos': 172, 'order': 43},
        {'type': 'var', 'content': '1', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 3, 'text_pos': 175, 'order': 44},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 3, 'text_pos': 176, 'order': 45},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 3, 'text_pos': 177, 'order': 46},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 3, 'text_pos': 178, 'order': 47},
        {'length': 3, 'hash': 48628067, 'line_pos': 55, 'line': 3, 'text_pos': 179, 'order': 48},
        {'length': 1, 'hash': 5, 'line_pos': 58, 'line': 3, 'text_pos': 182, 'order': 49},
        {'length': 1, 'hash': 4915261, 'line_pos': 0, 'line': 4, 'text_pos': 183, 'order': 50},
        {'length': 3, 'hash': 44302669, 'line_pos': 1, 'line': 4, 'text_pos': 184, 'order': 51},
        {'length': 1, 'hash': 4915261, 'line_pos': 4, 'line': 4, 'text_pos': 187, 'order': 52},
        {'length': 4, 'hash': 70451577, 'line_pos': 5, 'line': 4, 'text_pos': 188, 'order': 53},
        {'length': 12, 'hash': 4, 'line_pos': 9, 'line': 4, 'text_pos': 192, 'order': 54},
        {'type': 'var', 'content': '7092728', 'decsep': 'n', 'line_pos': 21, 'hash': 3, 'length': 7, 'line': 4, 'text_pos': 204, 'order': 55},
        {'length': 1, 'hash': 4, 'line_pos': 28, 'line': 4, 'text_pos': 211, 'order': 56},
        {'type': 'var', 'content': '6019072', 'decsep': 'n', 'line_pos': 29, 'hash': 3, 'length': 7, 'line': 4, 'text_pos': 212, 'order': 57},
        {'length': 6, 'hash': 4, 'line_pos': 36, 'line': 4, 'text_pos': 219, 'order': 58},
        {'type': 'var', 'content': '690324', 'decsep': 'n', 'line_pos': 42, 'hash': 3, 'length': 6, 'line': 4, 'text_pos': 225, 'order': 59},
        {'length': 2, 'hash': 4, 'line_pos': 48, 'line': 4, 'text_pos': 231, 'order': 60},
        {'type': 'var', 'content': '90', 'decsep': 'n', 'line_pos': 50, 'hash': 3, 'length': 2, 'line': 4, 'text_pos': 233, 'order': 61},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 4, 'text_pos': 235, 'order': 62},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 4, 'text_pos': 236, 'order': 63},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 4, 'text_pos': 237, 'order': 64},
        {'length': 1, 'hash': 5, 'line_pos': 55, 'line': 4, 'text_pos': 238, 'order': 65},
        {'length': 5, 'hash': 115016248, 'line_pos': 0, 'line': 5, 'text_pos': 239, 'order': 66},
        {'length': 16, 'hash': 4, 'line_pos': 5, 'line': 5, 'text_pos': 244, 'order': 67},
        {'type': 'var', 'content': '1542888', 'decsep': 'n', 'line_pos': 21, 'hash': 3, 'length': 7, 'line': 5, 'text_pos': 260, 'order': 68},
        {'length': 7, 'hash': 4, 'line_pos': 28, 'line': 5, 'text_pos': 267, 'order': 69},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 35, 'hash': 3, 'length': 1, 'line': 5, 'text_pos': 274, 'order': 70},
        {'length': 5, 'hash': 4, 'line_pos': 36, 'line': 5, 'text_pos': 275, 'order': 71},
        {'type': 'var', 'content': '1542888', 'decsep': 'n', 'line_pos': 41, 'hash': 3, 'length': 7, 'line': 5, 'text_pos': 280, 'order': 72},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 5, 'text_pos': 287, 'order': 73},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 5, 'text_pos': 290, 'order': 74},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 5, 'text_pos': 291, 'order': 75},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 5, 'text_pos': 292, 'order': 76},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 5, 'text_pos': 293, 'order': 77},
        {'length': 3, 'hash': 44302669, 'line_pos': 55, 'line': 5, 'text_pos': 294, 'order': 78},
        {'length': 1, 'hash': 4915261, 'line_pos': 58, 'line': 5, 'text_pos': 297, 'order': 79},
        {'length': 3, 'hash': 47055190, 'line_pos': 59, 'line': 5, 'text_pos': 298, 'order': 80},
        {'length': 1, 'hash': 5, 'line_pos': 62, 'line': 5, 'text_pos': 301, 'order': 81},
        {'length': 5, 'hash': 115016248, 'line_pos': 0, 'line': 6, 'text_pos': 302, 'order': 82},
        {'length': 16, 'hash': 4, 'line_pos': 5, 'line': 6, 'text_pos': 307, 'order': 83},
        {'type': 'var', 'content': '1542888', 'decsep': 'n', 'line_pos': 21, 'hash': 3, 'length': 7, 'line': 6, 'text_pos': 323, 'order': 84},
        {'length': 7, 'hash': 4, 'line_pos': 28, 'line': 6, 'text_pos': 330, 'order': 85},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 35, 'hash': 3, 'length': 1, 'line': 6, 'text_pos': 337, 'order': 86},
        {'length': 5, 'hash': 4, 'line_pos': 36, 'line': 6, 'text_pos': 338, 'order': 87},
        {'type': 'var', 'content': '1542888', 'decsep': 'n', 'line_pos': 41, 'hash': 3, 'length': 7, 'line': 6, 'text_pos': 343, 'order': 88},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 6, 'text_pos': 350, 'order': 89},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 6, 'text_pos': 353, 'order': 90},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 6, 'text_pos': 354, 'order': 91},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 6, 'text_pos': 355, 'order': 92},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 6, 'text_pos': 356, 'order': 93},
        {'length': 3, 'hash': 49676653, 'line_pos': 55, 'line': 6, 'text_pos': 357, 'order': 94},
        {'length': 1, 'hash': 4915261, 'line_pos': 58, 'line': 6, 'text_pos': 360, 'order': 95},
        {'length': 2, 'hash': 23658727, 'line_pos': 59, 'line': 6, 'text_pos': 361, 'order': 96},
        {'length': 1, 'hash': 4915261, 'line_pos': 61, 'line': 6, 'text_pos': 363, 'order': 97},
        {'length': 6, 'hash': 153485982, 'line_pos': 62, 'line': 6, 'text_pos': 364, 'order': 98},
        {'length': 1, 'hash': 5, 'line_pos': 68, 'line': 6, 'text_pos': 370, 'order': 99},
        {'length': 5, 'hash': 115016248, 'line_pos': 0, 'line': 7, 'text_pos': 371, 'order': 100},
        {'length': 16, 'hash': 4, 'line_pos': 5, 'line': 7, 'text_pos': 376, 'order': 101},
        {'type': 'var', 'content': '1542888', 'decsep': 'n', 'line_pos': 21, 'hash': 3, 'length': 7, 'line': 7, 'text_pos': 392, 'order': 102},
        {'length': 5, 'hash': 4, 'line_pos': 28, 'line': 7, 'text_pos': 399, 'order': 103},
        {'type': 'var', 'content': '532', 'decsep': 'n', 'line_pos': 33, 'hash': 3, 'length': 3, 'line': 7, 'text_pos': 404, 'order': 104},
        {'length': 5, 'hash': 4, 'line_pos': 36, 'line': 7, 'text_pos': 407, 'order': 105},
        {'type': 'var', 'content': '1542356', 'decsep': 'n', 'line_pos': 41, 'hash': 3, 'length': 7, 'line': 7, 'text_pos': 412, 'order': 106},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 7, 'text_pos': 419, 'order': 107},
        {'type': 'var', 'content': '1', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 7, 'text_pos': 422, 'order': 108},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 7, 'text_pos': 423, 'order': 109},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 7, 'text_pos': 424, 'order': 110},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 7, 'text_pos': 425, 'order': 111},
        {'length': 3, 'hash': 48103775, 'line_pos': 55, 'line': 7, 'text_pos': 426, 'order': 112},
        {'length': 1, 'hash': 5, 'line_pos': 58, 'line': 7, 'text_pos': 429, 'order': 113},
        {'length': 1, 'hash': 4915261, 'line_pos': 0, 'line': 8, 'text_pos': 430, 'order': 114},
        {'length': 3, 'hash': 44302669, 'line_pos': 1, 'line': 8, 'text_pos': 431, 'order': 115},
        {'length': 1, 'hash': 4915261, 'line_pos': 4, 'line': 8, 'text_pos': 434, 'order': 116},
        {'length': 4, 'hash': 70320503, 'line_pos': 5, 'line': 8, 'text_pos': 435, 'order': 117},
        {'length': 13, 'hash': 4, 'line_pos': 9, 'line': 8, 'text_pos': 439, 'order': 118},
        {'type': 'var', 'content': '516040', 'decsep': 'n', 'line_pos': 22, 'hash': 3, 'length': 6, 'line': 8, 'text_pos': 452, 'order': 119},
        {'length': 3, 'hash': 4, 'line_pos': 28, 'line': 8, 'text_pos': 458, 'order': 120},
        {'type': 'var', 'content': '37280', 'decsep': 'n', 'line_pos': 31, 'hash': 3, 'length': 5, 'line': 8, 'text_pos': 461, 'order': 121},
        {'length': 6, 'hash': 4, 'line_pos': 36, 'line': 8, 'text_pos': 466, 'order': 122},
        {'type': 'var', 'content': '452548', 'decsep': 'n', 'line_pos': 42, 'hash': 3, 'length': 6, 'line': 8, 'text_pos': 472, 'order': 123},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 8, 'text_pos': 478, 'order': 124},
        {'type': 'var', 'content': '8', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 8, 'text_pos': 481, 'order': 125},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 8, 'text_pos': 482, 'order': 126},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 8, 'text_pos': 483, 'order': 127},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 8, 'text_pos': 484, 'order': 128},
        {'length': 4, 'hash': 74252738, 'line_pos': 55, 'line': 8, 'text_pos': 485, 'order': 129},
        {'length': 1, 'hash': 5, 'line_pos': 59, 'line': 8, 'text_pos': 489, 'order': 130},
        {'length': 5, 'hash': 115016248, 'line_pos': 0, 'line': 9, 'text_pos': 490, 'order': 131},
        {'length': 17, 'hash': 4, 'line_pos': 5, 'line': 9, 'text_pos': 495, 'order': 132},
        {'type': 'var', 'content': '308580', 'decsep': 'n', 'line_pos': 22, 'hash': 3, 'length': 6, 'line': 9, 'text_pos': 512, 'order': 133},
        {'length': 7, 'hash': 4, 'line_pos': 28, 'line': 9, 'text_pos': 518, 'order': 134},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 35, 'hash': 3, 'length': 1, 'line': 9, 'text_pos': 525, 'order': 135},
        {'length': 6, 'hash': 4, 'line_pos': 36, 'line': 9, 'text_pos': 526, 'order': 136},
        {'type': 'var', 'content': '308580', 'decsep': 'n', 'line_pos': 42, 'hash': 3, 'length': 6, 'line': 9, 'text_pos': 532, 'order': 137},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 9, 'text_pos': 538, 'order': 138},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 9, 'text_pos': 541, 'order': 139},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 9, 'text_pos': 542, 'order': 140},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 9, 'text_pos': 543, 'order': 141},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 9, 'text_pos': 544, 'order': 142},
        {'length': 3, 'hash': 48628067, 'line_pos': 55, 'line': 9, 'text_pos': 545, 'order': 143},
        {'length': 1, 'hash': 4915261, 'line_pos': 58, 'line': 9, 'text_pos': 548, 'order': 144},
        {'length': 4, 'hash': 78578125, 'line_pos': 59, 'line': 9, 'text_pos': 549, 'order': 145},
        {'length': 1, 'hash': 4915261, 'line_pos': 63, 'line': 9, 'text_pos': 553, 'order': 146},
        {'type': 'var', 'content': '1001', 'decsep': 'n', 'line_pos': 64, 'hash': 3, 'length': 4, 'line': 9, 'text_pos': 554, 'order': 147},
        {'length': 1, 'hash': 5, 'line_pos': 68, 'line': 9, 'text_pos': 558, 'order': 148},
        {'length': 5, 'hash': 115016248, 'line_pos': 0, 'line': 10, 'text_pos': 559, 'order': 149},
        {'length': 17, 'hash': 4, 'line_pos': 5, 'line': 10, 'text_pos': 564, 'order': 150},
        {'type': 'var', 'content': '308580', 'decsep': 'n', 'line_pos': 22, 'hash': 3, 'length': 6, 'line': 10, 'text_pos': 581, 'order': 151},
        {'length': 7, 'hash': 4, 'line_pos': 28, 'line': 10, 'text_pos': 587, 'order': 152},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 35, 'hash': 3, 'length': 1, 'line': 10, 'text_pos': 594, 'order': 153},
        {'length': 6, 'hash': 4, 'line_pos': 36, 'line': 10, 'text_pos': 595, 'order': 154},
        {'type': 'var', 'content': '308580', 'decsep': 'n', 'line_pos': 42, 'hash': 3, 'length': 6, 'line': 10, 'text_pos': 601, 'order': 155},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 10, 'text_pos': 607, 'order': 156},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 10, 'text_pos': 610, 'order': 157},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 10, 'text_pos': 611, 'order': 158},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 10, 'text_pos': 612, 'order': 159},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 10, 'text_pos': 613, 'order': 160},
        {'length': 3, 'hash': 48628067, 'line_pos': 55, 'line': 10, 'text_pos': 614, 'order': 161},
        {'length': 1, 'hash': 4915261, 'line_pos': 58, 'line': 10, 'text_pos': 617, 'order': 162},
        {'length': 4, 'hash': 78578125, 'line_pos': 59, 'line': 10, 'text_pos': 618, 'order': 163},
        {'length': 1, 'hash': 4915261, 'line_pos': 63, 'line': 10, 'text_pos': 622, 'order': 164},
        {'type': 'var', 'content': '1000', 'decsep': 'n', 'line_pos': 64, 'hash': 3, 'length': 4, 'line': 10, 'text_pos': 623, 'order': 165},
        {'length': 1, 'hash': 5, 'line_pos': 68, 'line': 10, 'text_pos': 627, 'order': 166},
        {'length': 5, 'hash': 115016248, 'line_pos': 0, 'line': 11, 'text_pos': 628, 'order': 167},
        {'length': 17, 'hash': 4, 'line_pos': 5, 'line': 11, 'text_pos': 633, 'order': 168},
        {'type': 'var', 'content': '308580', 'decsep': 'n', 'line_pos': 22, 'hash': 3, 'length': 6, 'line': 11, 'text_pos': 650, 'order': 169},
        {'length': 7, 'hash': 4, 'line_pos': 28, 'line': 11, 'text_pos': 656, 'order': 170},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 35, 'hash': 3, 'length': 1, 'line': 11, 'text_pos': 663, 'order': 171},
        {'length': 6, 'hash': 4, 'line_pos': 36, 'line': 11, 'text_pos': 664, 'order': 172},
        {'type': 'var', 'content': '308580', 'decsep': 'n', 'line_pos': 42, 'hash': 3, 'length': 6, 'line': 11, 'text_pos': 670, 'order': 173},
        {'length': 3, 'hash': 4, 'line_pos': 48, 'line': 11, 'text_pos': 676, 'order': 174},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 51, 'hash': 3, 'length': 1, 'line': 11, 'text_pos': 679, 'order': 175},
        {'length': 1, 'hash': 4259891, 'line_pos': 52, 'line': 11, 'text_pos': 680, 'order': 176},
        {'length': 1, 'hash': 4, 'line_pos': 53, 'line': 11, 'text_pos': 681, 'order': 177},
        {'length': 1, 'hash': 4915261, 'line_pos': 54, 'line': 11, 'text_pos': 682, 'order': 178},
        {'length': 3, 'hash': 48628067, 'line_pos': 55, 'line': 11, 'text_pos': 683, 'order': 179},
        {'length': 1, 'hash': 4915261, 'line_pos': 58, 'line': 11, 'text_pos': 686, 'order': 180},
        {'length': 4, 'hash': 78578125, 'line_pos': 59, 'line': 11, 'text_pos': 687, 'order': 181},
        {'length': 1, 'hash': 4915261, 'line_pos': 63, 'line': 11, 'text_pos': 691, 'order': 182},
        {'type': 'var', 'content': '0', 'decsep': 'n', 'line_pos': 64, 'hash': 3, 'length': 1, 'line': 11, 'text_pos': 692, 'order': 183},
        {'length': 1, 'hash': 5, 'line_pos': 65, 'line': 11, 'text_pos': 693, 'order': 184}
        ]}
        hashed_text2=varapi.get_hashed_text(text)
        self.assertTrue('elements' in hashed_text2)
        self.assertTrue('header_lines' in hashed_text2)
        self.assertEqual(hashed_text2['header_lines'],hashed_text['header_lines'])
        self.assertEqual(len(hashed_text2['elements']),len(hashed_text['elements']))
        self.assertEqual(hashed_text2['elements'],hashed_text['elements'])

    def test_get_variables_atts_success(self):
        ''' get_variables_atts should return the attributes associated to every text variable to identify uniquely in the text '''
        text='S.ficheros     bloques de 1K  Usados Disponibles Uso% Montado en\ndev                  1540336       0     1540336   0% /dev\nrun                  1542888     516     1542372   1% /run\n/dev/sda3            7092728 6019072      690324  90% /\ntmpfs                1542888       0     1542888   0% /dev/shm\ntmpfs                1542888       0     1542888   0% /sys/fs/cgroup\ntmpfs                1542888     532     1542356   1% /tmp\n/dev/sda1             516040   37280      452548   8% /boot\ntmpfs                 308580       0      308580   0% /run/user/1001\ntmpfs                 308580       0      308580   0% /run/user/1000\ntmpfs                 308580       0      308580   0% /run/user/0\n'
        var_atts=[{'text_pos': 86, 'atts': {'r_-8': 4259891, 'r_-11': 451675274, 'r_-1': 4, 'r_-20': 4, 'r_-9': 42729797, 'r_-13': 144704125, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'r_-6': 192217824, 'r_-16': 4, 'r_-10': 4, 'l_9': 4915261, 'r_-17': 22479063, 'c_-1': 204538633, 'l_5': 4, 'l_11': 5, 'r_-18': 4, 'r_-2': 44302669, 'r_-19': 204538633, 'r_-3': 5, 'c_1': 0, 'r_-7': 4, 'l_1': 4, 'l_4': 3, 'r_-4': 23199969, 'l_7': 4259891, 'r_-15': 14090378, 'l_-2': 44302669, 'r_-12': 4, 'l_6': 3, 'l_10': 44302669, 'l_8': 4, 'l_3': 4, 'r_-5': 4}},
        {'text_pos': 100, 'atts': {'l_-4': 44302669, 'r_-8': 192217824, 'r_-11': 42729797, 'l_-3': 4, 'r_-20': 4, 'r_-9': 4, 'r_-13': 451675274, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'r_-6': 23199969, 'r_-16': 4, 'r_-10': 4259891, 'l_9': 5, 'r_-17': 14090378, 'c_-1': 144704125, 'l_5': 4259891, 'r_-18': 4, 'r_-1': 4, 'r_-2': 3, 'r_-19': 22479063, 'r_-3': 4, 'c_1': 0, 'r_-7': 4, 'l_1': 4, 'l_4': 3, 'r_-4': 44302669, 'l_7': 4915261, 'r_-15': 144704125, 'l_-2': 3, 'r_-12': 4, 'l_6': 4, 'l_8': 44302669, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 106, 'atts': {'l_-6': 44302669, 'r_-8': 23199969, 'r_-11': 4, 'l_-3': 4, 'r_-20': 4, 'r_-9': 4, 'r_-13': 42729797, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4, 'r_-19': 14090378, 'r_-16': 4, 'r_-10': 192217824, 'r_-17': 144704125, 'c_-1': 451675274, 'l_5': 4915261, 'r_-18': 4, 'r_-6': 44302669, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 5, 'r_-15': 451675274, 'l_-2': 3, 'r_-12': 4259891, 'l_6': 44302669, 'r_-1': 4, 'c_1': 0, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 116, 'atts': {'l_-6': 3, 'r_-8': 44302669, 'r_-11': 4, 'r_-4': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4, 'l_-7': 4, 'r_-13': 4, 'l_2': 4, 'l_-1': 4, 'r_-14': 4259891, 'l_-5': 4, 'r_-19': 144704125, 'r_-10': 23199969, 'r_-17': 451675274, 'c_-1': 42729797, 'l_5': 5, 'r_-18': 4, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4, 'l_1': 4259891, 'l_4': 44302669, 'l_-8': 44302669, 'r_-15': 42729797, 'l_-2': 3, 'r_-12': 192217824, 'r_-9': 5, 'r_-1': 4, 'c_1': 0, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 145, 'atts': {'r_-8': 3, 'r_-11': 4, 'r_-1': 4, 'r_-20': 192217824, 'r_-9': 4, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 4, 'r_-16': 44302669, 'r_-10': 3, 'l_9': 4915261, 'r_-17': 5, 'c_-1': 204538633, 'l_5': 4, 'l_11': 5, 'r_-18': 23199969, 'r_-2': 48628067, 'r_-19': 4, 'r_-3': 5, 'c_1': 0, 'r_-7': 4259891, 'l_1': 4, 'l_4': 3, 'r_-4': 44302669, 'l_7': 4259891, 'r_-15': 4, 'l_-2': 48628067, 'r_-12': 3, 'l_6': 3, 'l_10': 48628067, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 157, 'atts': {'l_-4': 48628067, 'r_-8': 4, 'r_-11': 4, 'l_-3': 4, 'r_-20': 23199969, 'r_-9': 4259891, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 44302669, 'r_-16': 3, 'r_-10': 3, 'l_9': 5, 'r_-17': 4, 'c_-1': 144704125, 'l_5': 4259891, 'r_-18': 44302669, 'r_-1': 4, 'r_-2': 3, 'r_-19': 5, 'r_-3': 4, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 48628067, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 3, 'l_6': 4, 'l_8': 48628067, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 165, 'atts': {'l_-6': 48628067, 'r_-8': 44302669, 'r_-11': 4259891, 'l_-3': 4, 'r_-20': 44302669, 'r_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'l_-5': 4, 'r_-19': 4, 'r_-16': 3, 'r_-10': 4, 'r_-17': 4, 'c_-1': 451675274, 'l_5': 4915261, 'r_-18': 3, 'r_-6': 48628067, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 5, 'r_-15': 4, 'l_-2': 3, 'r_-12': 3, 'l_6': 48628067, 'r_-1': 4, 'c_1': 0, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 175, 'atts': {'l_-6': 3, 'r_-8': 48628067, 'r_-11': 4915261, 'r_-4': 3, 'l_-3': 4, 'r_-16': 3, 'r_-20': 3, 'l_-7': 4, 'r_-13': 4259891, 'l_2': 4, 'l_-1': 4, 'r_-14': 3, 'l_-5': 4, 'r_-19': 4, 'r_-10': 44302669, 'r_-17': 4, 'c_-1': 42729797, 'l_5': 5, 'r_-18': 3, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4, 'l_1': 4259891, 'l_4': 48628067, 'l_-8': 48628067, 'r_-15': 4, 'l_-2': 3, 'r_-12': 4, 'r_-9': 5, 'r_-1': 4, 'c_1': 0, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 204, 'atts': {'r_-19': 48628067, 'r_-8': 4915261, 'r_-11': 3, 'l_-3': 4915261, 'r_-1': 4, 'r_-20': 5, 'r_-9': 4, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4915261, 'r_-6': 5, 'r_-16': 4, 'r_-10': 4259891, 'l_9': 4915261, 'r_-17': 3, 'c_-1': 204538633, 'l_5': 4, 'r_-18': 4, 'r_-2': 70451577, 'l_-4': 44302669, 'r_-3': 4915261, 'c_1': 0, 'r_-7': 48628067, 'l_1': 4, 'l_4': 3, 'r_-4': 44302669, 'l_7': 4259891, 'r_-15': 3, 'l_-2': 70451577, 'r_-12': 4, 'l_6': 3, 'l_10': 5, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 212, 'atts': {'l_-6': 44302669, 'r_-8': 5, 'r_-11': 4, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4, 'l_-7': 4915261, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4915261, 'r_-19': 3, 'r_-10': 4915261, 'r_-17': 3, 'c_-1': 4, 'l_5': 4259891, 'r_-18': 4, 'r_-6': 44302669, 'r_-2': 3, 'r_-9': 48628067, 'l_-4': 70451577, 'r_-3': 4, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 70451577, 'l_7': 4915261, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4259891, 'l_6': 4, 'r_-1': 4, 'l_8': 5, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 225, 'atts': {'l_-6': 70451577, 'r_-8': 44302669, 'r_-11': 48628067, 'r_-4': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4, 'l_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 4259891, 'l_-5': 4, 'r_-19': 3, 'r_-10': 5, 'r_-17': 3, 'c_-1': 451675274, 'l_5': 4915261, 'r_-18': 4, 'r_-6': 70451577, 'r_-2': 3, 'r_-9': 4915261, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4915261, 'l_1': 4, 'l_4': 4, 'l_-8': 44302669, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4915261, 'l_6': 5, 'r_-1': 4, 'c_1': 0, 'l_3': 4259891, 'l_-7': 4915261, 'r_-5': 4}},
        {'text_pos': 233, 'atts': {'l_-6': 3, 'r_-8': 70451577, 'r_-11': 4915261, 'l_-9': 4915261, 'l_-3': 4, 'l_-11': 4915261, 'r_-16': 4259891, 'r_-20': 4, 'l_-7': 4, 'r_-13': 48628067, 'l_2': 4, 'l_-1': 4, 'r_-14': 4915261, 'l_-5': 4, 'r_-19': 3, 'r_-10': 44302669, 'r_-1': 4, 'r_-17': 3, 'c_-1': 42729797, 'r_-9': 4915261, 'r_-18': 4, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4, 'l_1': 4259891, 'l_4': 5, 'l_-8': 70451577, 'r_-15': 4, 'l_-2': 3, 'r_-12': 5, 'r_-4': 3, 'l_-10': 44302669, 'c_1': 0, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 260, 'atts': {'l_13': 5, 'r_-8': 4, 'r_-11': 3, 'l_12': 47055190, 'r_-1': 4, 'r_-20': 48628067, 'r_-9': 3, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'r_-6': 4259891, 'r_-16': 4915261, 'r_-10': 4, 'l_9': 4915261, 'r_-17': 44302669, 'c_-1': 204538633, 'l_5': 4, 'l_11': 4915261, 'r_-18': 4915261, 'r_-2': 115016248, 'r_-19': 5, 'r_-3': 5, 'c_1': 0, 'r_-7': 3, 'l_1': 4, 'l_4': 3, 'r_-4': 4915261, 'l_7': 4259891, 'r_-15': 70451577, 'l_-2': 115016248, 'r_-12': 4, 'l_6': 3, 'l_10': 44302669, 'l_8': 4, 'l_3': 4, 'r_-5': 4}},
        {'text_pos': 274, 'atts': {'r_-19': 44302669, 'r_-8': 4259891, 'r_-11': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4915261, 'r_-9': 3, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'r_-6': 4915261, 'r_-10': 4, 'l_9': 4915261, 'r_-17': 70451577, 'c_-1': 144704125, 'l_5': 4259891, 'l_11': 5, 'r_-18': 4915261, 'r_-1': 4, 'r_-2': 3, 'l_-4': 115016248, 'r_-3': 4, 'c_1': 0, 'r_-7': 4, 'l_1': 4, 'l_4': 3, 'r_-4': 115016248, 'l_7': 4915261, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4, 'l_6': 4, 'l_10': 47055190, 'l_8': 44302669, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 280, 'atts': {'l_-6': 115016248, 'r_-8': 4915261, 'r_-11': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4915261, 'r_-9': 4, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4, 'r_-19': 70451577, 'r_-10': 4259891, 'l_9': 5, 'r_-17': 3, 'c_-1': 451675274, 'l_5': 4915261, 'r_-18': 4, 'r_-6': 115016248, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 4915261, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4, 'l_6': 44302669, 'r_-1': 4, 'l_8': 47055190, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 290, 'atts': {'l_-6': 3, 'r_-8': 115016248, 'r_-11': 4, 'r_-4': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4, 'r_-9': 5, 'l_-7': 4, 'r_-13': 3, 'l_2': 4, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4, 'r_-19': 3, 'r_-10': 4915261, 'r_-17': 3, 'c_-1': 42729797, 'l_5': 4915261, 'r_-18': 4, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4, 'l_1': 4259891, 'l_4': 44302669, 'l_-8': 115016248, 'l_7': 5, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4259891, 'l_6': 47055190, 'r_-1': 4, 'c_1': 0, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 323, 'atts': {'l_13': 4915261, 'l_15': 5, 'r_-8': 4, 'r_-11': 4, 'l_12': 23658727, 'l_14': 153485982, 'r_-20': 4915261, 'r_-9': 4259891, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 44302669, 'r_-16': 3, 'r_-10': 3, 'l_9': 4915261, 'r_-17': 4, 'c_-1': 204538633, 'l_5': 4, 'l_11': 4915261, 'r_-18': 115016248, 'r_-1': 4, 'r_-2': 115016248, 'r_-19': 5, 'r_-3': 5, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 47055190, 'l_7': 4259891, 'r_-15': 4, 'l_-2': 115016248, 'r_-12': 3, 'l_6': 3, 'l_10': 49676653, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 337, 'atts': {'l_13': 5, 'r_-8': 44302669, 'r_-11': 4259891, 'l_12': 153485982, 'l_-3': 4, 'r_-1': 4, 'r_-16': 3, 'r_-20': 115016248, 'r_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-19': 4, 'r_-10': 4, 'l_9': 4915261, 'r_-17': 4, 'c_-1': 144704125, 'l_5': 4259891, 'l_11': 4915261, 'r_-18': 3, 'r_-6': 47055190, 'r_-2': 3, 'l_-4': 115016248, 'r_-3': 4, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 115016248, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 3, 'l_6': 4, 'l_10': 23658727, 'l_8': 49676653, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 343, 'atts': {'l_-6': 115016248, 'r_-8': 47055190, 'r_-11': 4915261, 'l_-3': 4, 'r_-16': 3, 'r_-20': 3, 'r_-9': 4915261, 'r_-13': 4259891, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'l_-5': 4, 'r_-19': 4, 'r_-10': 44302669, 'l_9': 4915261, 'r_-1': 4, 'r_-17': 4, 'c_-1': 451675274, 'l_5': 4915261, 'l_11': 5, 'r_-18': 3, 'r_-6': 115016248, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 4, 'l_6': 49676653, 'l_10': 153485982, 'l_8': 23658727, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 353, 'atts': {'l_-6': 3, 'r_-8': 115016248, 'r_-11': 4915261, 'r_-4': 3, 'l_-3': 4, 'r_-16': 3, 'r_-20': 3, 'r_-9': 5, 'l_-7': 4, 'r_-13': 4915261, 'l_2': 4, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4, 'r_-19': 4, 'r_-10': 47055190, 'l_9': 5, 'r_-17': 4, 'c_-1': 42729797, 'l_5': 4915261, 'r_-18': 3, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 4, 'l_1': 4259891, 'l_4': 49676653, 'l_-8': 115016248, 'l_7': 4915261, 'r_-15': 4259891, 'l_-2': 3, 'r_-12': 44302669, 'l_6': 23658727, 'r_-1': 4, 'l_8': 153485982, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 392, 'atts': {'r_-8': 49676653, 'r_-11': 4259891, 'r_-1': 4, 'r_-20': 115016248, 'r_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 23658727, 'r_-16': 3, 'r_-10': 4, 'l_9': 4915261, 'r_-17': 4, 'c_-1': 204538633, 'l_5': 4, 'l_11': 5, 'r_-18': 3, 'r_-2': 115016248, 'r_-19': 4, 'r_-3': 5, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 153485982, 'l_7': 4259891, 'r_-15': 4, 'l_-2': 115016248, 'r_-12': 3, 'l_6': 3, 'l_10': 48103775, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 404, 'atts': {'l_-4': 115016248, 'r_-8': 23658727, 'r_-11': 4915261, 'l_-3': 4, 'r_-20': 3, 'r_-9': 4915261, 'r_-13': 4259891, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 153485982, 'r_-16': 3, 'r_-10': 49676653, 'l_9': 5, 'r_-17': 4, 'c_-1': 144704125, 'l_5': 4259891, 'r_-18': 3, 'r_-1': 4, 'r_-2': 3, 'r_-19': 4, 'r_-3': 4, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 115016248, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 4, 'l_6': 4, 'l_8': 48103775, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 412, 'atts': {'l_-6': 115016248, 'r_-8': 153485982, 'r_-11': 4915261, 'l_-3': 4, 'r_-20': 3, 'r_-9': 4915261, 'r_-13': 4915261, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4, 'r_-19': 4, 'r_-16': 3, 'r_-10': 23658727, 'r_-17': 4, 'c_-1': 451675274, 'l_5': 4915261, 'r_-18': 3, 'r_-6': 115016248, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 5, 'r_-15': 4259891, 'l_-2': 3, 'r_-12': 49676653, 'l_6': 48103775, 'r_-1': 4, 'c_1': 0, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 422, 'atts': {'l_-6': 3, 'r_-8': 115016248, 'r_-11': 4915261, 'r_-4': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 3, 'l_-7': 4, 'r_-13': 4915261, 'l_2': 4, 'l_-1': 4, 'r_-14': 49676653, 'l_-5': 4, 'r_-19': 4, 'r_-10': 153485982, 'r_-17': 4259891, 'c_-1': 42729797, 'l_5': 5, 'r_-18': 3, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4, 'l_1': 4259891, 'l_4': 48103775, 'l_-8': 115016248, 'r_-15': 4915261, 'l_-2': 3, 'r_-12': 23658727, 'r_-9': 5, 'r_-1': 4, 'c_1': 0, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 452, 'atts': {'r_-19': 115016248, 'r_-8': 4915261, 'r_-11': 3, 'l_-3': 4915261, 'r_-1': 4, 'r_-20': 5, 'r_-9': 4, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4915261, 'r_-6': 5, 'r_-16': 4, 'r_-10': 4259891, 'l_9': 4915261, 'r_-17': 3, 'c_-1': 4, 'l_5': 4, 'l_11': 5, 'r_-18': 4, 'r_-2': 70320503, 'l_-4': 44302669, 'r_-3': 4915261, 'c_1': 0, 'r_-7': 48103775, 'l_1': 4, 'l_4': 3, 'r_-4': 44302669, 'l_7': 4259891, 'r_-15': 3, 'l_-2': 70320503, 'r_-12': 4, 'l_6': 3, 'l_10': 74252738, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 461, 'atts': {'l_-6': 44302669, 'r_-8': 5, 'r_-11': 4, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4, 'l_-7': 4915261, 'r_-13': 3, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4915261, 'r_-19': 3, 'r_-10': 4915261, 'l_9': 5, 'r_-17': 3, 'c_-1': 144704125, 'l_5': 4259891, 'r_-18': 4, 'r_-6': 44302669, 'r_-2': 3, 'r_-9': 48103775, 'l_-4': 70320503, 'r_-3': 4, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 70320503, 'l_7': 4915261, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4259891, 'l_6': 4, 'r_-1': 4, 'l_8': 74252738, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 472, 'atts': {'l_-6': 70320503, 'r_-8': 44302669, 'r_-11': 48103775, 'r_-4': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 4, 'l_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 4259891, 'l_-5': 4, 'r_-19': 3, 'r_-10': 5, 'r_-17': 3, 'c_-1': 451675274, 'l_5': 4915261, 'r_-18': 4, 'r_-6': 70320503, 'r_-2': 3, 'r_-9': 4915261, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4915261, 'l_1': 4, 'l_4': 4, 'l_-8': 44302669, 'l_7': 5, 'r_-15': 3, 'l_-2': 3, 'r_-12': 4915261, 'l_6': 74252738, 'r_-1': 4, 'c_1': 0, 'l_3': 4259891, 'l_-7': 4915261, 'r_-5': 4}},
        {'text_pos': 481, 'atts': {'l_-6': 3, 'r_-8': 70320503, 'r_-11': 4915261, 'l_-9': 4915261, 'l_-3': 4, 'l_-11': 4915261, 'r_-16': 4259891, 'r_-20': 4, 'l_-7': 4, 'r_-13': 48103775, 'l_2': 4, 'l_-1': 4, 'r_-14': 4915261, 'l_-5': 4, 'r_-19': 3, 'r_-10': 44302669, 'r_-1': 4, 'r_-4': 3, 'r_-17': 3, 'c_-1': 42729797, 'l_5': 5, 'r_-18': 4, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'r_-7': 4, 'l_1': 4259891, 'l_4': 74252738, 'l_-8': 70320503, 'r_-15': 4, 'l_-2': 3, 'r_-12': 5, 'r_-9': 4915261, 'l_-10': 44302669, 'c_1': 0, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 512, 'atts': {'l_13': 4915261, 'l_15': 5, 'r_-8': 3, 'r_-11': 4, 'r_-20': 5, 'l_14': 3, 'l_12': 78578125, 'r_-9': 4, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 4, 'r_-16': 70320503, 'r_-10': 3, 'l_9': 4915261, 'r_-17': 4915261, 'c_-1': 4, 'l_5': 4, 'l_11': 4915261, 'r_-18': 44302669, 'r_-1': 4, 'r_-2': 115016248, 'r_-19': 4915261, 'r_-3': 5, 'c_1': 0, 'r_-7': 4259891, 'l_1': 4, 'l_4': 3, 'r_-4': 74252738, 'l_7': 4259891, 'r_-15': 4, 'l_-2': 115016248, 'r_-12': 3, 'l_6': 3, 'l_10': 48628067, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 525, 'atts': {'l_13': 5, 'r_-8': 4, 'r_-11': 4, 'r_-20': 44302669, 'l_-3': 4, 'r_-1': 4, 'r_-16': 3, 'l_12': 3, 'r_-9': 4259891, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'c_1': 0, 'r_-19': 4915261, 'r_-10': 3, 'l_9': 4915261, 'r_-17': 4, 'c_-1': 144704125, 'l_5': 4259891, 'l_11': 4915261, 'r_-18': 70320503, 'r_-6': 74252738, 'r_-2': 3, 'l_-4': 115016248, 'r_-3': 4, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 115016248, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 3, 'l_6': 4, 'l_10': 78578125, 'l_8': 48628067, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 532, 'atts': {'l_-6': 115016248, 'r_-8': 74252738, 'r_-11': 4259891, 'l_-3': 4, 'r_-16': 3, 'r_-20': 70320503, 'r_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'l_-5': 4, 'r_-19': 4, 'r_-10': 4, 'l_9': 4915261, 'r_-1': 4, 'r_-17': 4, 'c_-1': 451675274, 'l_5': 4915261, 'l_11': 5, 'r_-18': 3, 'r_-6': 115016248, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 3, 'l_6': 48628067, 'l_10': 3, 'l_8': 78578125, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 541, 'atts': {'l_-6': 3, 'r_-8': 115016248, 'r_-11': 4915261, 'r_-4': 3, 'l_-3': 4, 'r_-16': 3, 'r_-20': 3, 'r_-9': 5, 'l_-7': 4, 'r_-13': 4259891, 'l_2': 4, 'l_-1': 4, 'r_-14': 3, 'l_-5': 4, 'r_-19': 4, 'r_-10': 74252738, 'l_9': 5, 'r_-17': 4, 'c_-1': 42729797, 'l_5': 4915261, 'r_-18': 3, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 4, 'l_1': 4259891, 'l_4': 48628067, 'l_-8': 115016248, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 4, 'l_6': 78578125, 'r_-1': 4, 'l_8': 3, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 554, 'atts': {'l_-6': 4, 'r_-7': 4259891, 'r_-8': 3, 'r_-11': 4, 'r_-4': 48628067, 'l_-3': 4915261, 'l_-11': 4, 'r_-1': 4915261, 'r_-20': 4, 'l_-9': 4, 'r_-13': 4, 'l_-12': 3, 'l_-1': 4915261, 'r_-14': 3, 'l_-5': 4915261, 'l_-7': 4259891, 'r_-16': 115016248, 'r_-10': 3, 'l_-15': 4, 'r_-17': 5, 'c_-1': 5, 'r_-9': 4, 'r_-5': 4915261, 'r_-18': 74252738, 'r_-6': 4, 'r_-2': 78578125, 'l_-4': 48628067, 'r_-3': 4915261, 'l_-14': 3, 'r_-19': 4915261, 'l_1': 5, 'l_-8': 3, 'r_-15': 4, 'l_-2': 78578125, 'r_-12': 3, 'l_-16': 115016248, 'l_-10': 3, 'c_1': 0, 'l_-13': 4}},
        {'text_pos': 581, 'atts': {'l_13': 4915261, 'l_15': 5, 'r_-8': 48628067, 'r_-11': 4259891, 'r_-20': 115016248, 'l_14': 3, 'l_12': 78578125, 'r_-9': 4915261, 'r_-13': 4, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 78578125, 'r_-16': 3, 'r_-10': 4, 'l_9': 4915261, 'r_-17': 4, 'c_-1': 4, 'l_5': 4, 'l_11': 4915261, 'r_-18': 3, 'r_-1': 4, 'r_-2': 115016248, 'r_-19': 4, 'r_-3': 5, 'c_1': 0, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 3, 'l_7': 4259891, 'r_-15': 4, 'l_-2': 115016248, 'r_-12': 3, 'l_6': 3, 'l_10': 48628067, 'l_8': 4, 'l_3': 4, 'r_-5': 4915261}},
        {'text_pos': 594, 'atts': {'l_13': 5, 'r_-8': 78578125, 'r_-11': 4915261, 'r_-20': 3, 'l_-3': 4, 'r_-1': 4, 'r_-16': 3, 'l_12': 3, 'r_-9': 4915261, 'r_-13': 4259891, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'c_1': 0, 'r_-19': 4, 'r_-10': 48628067, 'l_9': 4915261, 'r_-17': 4, 'c_-1': 144704125, 'l_5': 4259891, 'l_11': 4915261, 'r_-18': 3, 'r_-6': 3, 'r_-2': 3, 'l_-4': 115016248, 'r_-3': 4, 'r_-7': 4915261, 'l_1': 4, 'l_4': 3, 'r_-4': 115016248, 'l_7': 4915261, 'r_-15': 4, 'l_-2': 3, 'r_-12': 4, 'l_6': 4, 'l_10': 78578125, 'l_8': 48628067, 'l_3': 4, 'r_-5': 5}},
        {'text_pos': 601, 'atts': {'l_-6': 115016248, 'r_-8': 3, 'r_-11': 4915261, 'l_-3': 4, 'r_-16': 3, 'r_-20': 3, 'r_-9': 4915261, 'r_-13': 4915261, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'l_-5': 4, 'r_-19': 4, 'r_-10': 78578125, 'l_9': 4915261, 'r_-1': 4, 'r_-17': 4, 'c_-1': 451675274, 'l_5': 4915261, 'l_11': 5, 'r_-18': 3, 'r_-6': 115016248, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 5, 'l_1': 4, 'l_4': 4, 'r_-4': 3, 'l_7': 4915261, 'r_-15': 4259891, 'l_-2': 3, 'r_-12': 48628067, 'l_6': 48628067, 'l_10': 3, 'l_8': 78578125, 'l_3': 4259891, 'r_-5': 4}},
        {'text_pos': 610, 'atts': {'l_-6': 3, 'r_-8': 115016248, 'r_-11': 4915261, 'r_-4': 3, 'l_-3': 4, 'r_-16': 4, 'r_-20': 3, 'r_-9': 5, 'l_-7': 4, 'r_-13': 4915261, 'l_2': 4, 'l_-1': 4, 'r_-14': 48628067, 'l_-5': 4, 'r_-19': 4, 'r_-10': 3, 'l_9': 5, 'r_-17': 4259891, 'c_-1': 42729797, 'l_5': 4915261, 'r_-18': 3, 'r_-6': 3, 'r_-2': 3, 'l_-4': 3, 'r_-3': 4, 'c_1': 0, 'r_-7': 4, 'l_1': 4259891, 'l_4': 48628067, 'l_-8': 115016248, 'l_7': 4915261, 'r_-15': 4915261, 'l_-2': 3, 'r_-12': 78578125, 'l_6': 78578125, 'r_-1': 4, 'l_8': 3, 'l_3': 4915261, 'r_-5': 4}},
        {'text_pos': 623, 'atts': {'r_-19': 4915261, 'r_-1': 4915261, 'l_-7': 4259891, 'r_-13': 4, 'l_-12': 3, 'r_-4': 48628067, 'l_-5': 4915261, 'l_-14': 3, 'r_-17': 5, 'c_-1': 5, 'r_-18': 3, 'l_-4': 48628067, 'r_-3': 4915261, 'l_-15': 4, 'l_-8': 3, 'r_-12': 3, 'c_1': 0, 'l_-13': 4, 'l_-6': 4, 'l_-2': 78578125, 'r_-8': 3, 'r_-11': 4, 'l_-3': 4915261, 'l_-11': 4, 'r_-20': 78578125, 'l_-9': 4, 'l_-1': 4915261, 'r_-14': 3, 'r_-9': 4, 'r_-16': 115016248, 'r_-10': 3, 'r_-15': 4, 'r_-6': 4, 'r_-2': 78578125, 'l_1': 5, 'r_-5': 4915261, 'l_-16': 115016248, 'l_-10': 3, 'r_-7': 4259891}},
        {'text_pos': 650, 'atts': {'l_13': 4915261, 'l_15': 5, 'l_14': 3, 'r_-13': 4, 'r_-4': 3, 'r_-17': 4, 'c_-1': 4, 'l_5': 4, 'l_11': 4915261, 'r_-18': 3, 'r_-19': 4, 'r_-3': 5, 'r_-12': 3, 'c_1': 0, 'l_3': 4, 'r_-1': 4, 'r_-8': 48628067, 'r_-11': 4259891, 'l_12': 78578125, 'r_-20': 115016248, 'r_-9': 4915261, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 78578125, 'r_-16': 3, 'r_-10': 4, 'l_9': 4915261, 'r_-15': 4, 'r_-2': 115016248, 'l_1': 4, 'l_4': 3, 'l_7': 4259891, 'r_-5': 4915261, 'l_-2': 115016248, 'l_6': 3, 'l_10': 48628067, 'l_8': 4, 'r_-7': 4915261}},
        {'text_pos': 663, 'atts': {'l_13': 5, 'r_-1': 4, 'r_-13': 4259891, 'r_-4': 115016248, 'r_-17': 4, 'c_-1': 144704125, 'l_5': 4259891, 'l_11': 4915261, 'r_-18': 3, 'r_-19': 4, 'r_-3': 4, 'l_-4': 115016248, 'r_-12': 4, 'c_1': 0, 'l_3': 4, 'r_-8': 78578125, 'r_-11': 4915261, 'l_12': 3, 'l_-3': 4, 'r_-20': 3, 'r_-9': 4915261, 'l_2': 3, 'l_-1': 4, 'r_-14': 3, 'r_-6': 3, 'r_-16': 3, 'r_-10': 48628067, 'l_9': 4915261, 'r_-15': 4, 'r_-2': 3, 'l_1': 4, 'l_4': 3, 'l_7': 4915261, 'r_-5': 5, 'l_-2': 3, 'l_6': 4, 'l_10': 78578125, 'l_8': 48628067, 'r_-7': 4915261}},
        {'text_pos': 670, 'atts': {'l_-4': 3, 'r_-1': 4, 'r_-13': 4915261, 'r_-4': 3, 'l_-5': 4, 'r_-17': 4, 'c_-1': 451675274, 'l_5': 4915261, 'l_11': 5, 'r_-18': 3, 'r_-19': 4, 'r_-3': 4, 'r_-12': 48628067, 'c_1': 0, 'l_3': 4259891, 'l_-6': 115016248, 'r_-8': 3, 'r_-11': 4915261, 'l_-3': 4, 'r_-20': 3, 'r_-9': 4915261, 'l_2': 3, 'l_-1': 4, 'r_-14': 4, 'r_-6': 115016248, 'r_-16': 3, 'r_-10': 78578125, 'l_9': 4915261, 'l_6': 48628067, 'r_-15': 4259891, 'r_-2': 3, 'l_1': 4, 'l_4': 4, 'l_7': 4915261, 'r_-5': 4, 'l_-2': 3, 'l_10': 3, 'l_8': 78578125, 'r_-7': 5}},
        {'text_pos': 679, 'atts': {'l_-4': 3, 'r_-1': 4, 'l_-7': 4, 'r_-4': 3, 'l_-5': 4, 'r_-17': 4259891, 'c_-1': 42729797, 'l_5': 4915261, 'l_9': 5, 'r_-18': 3, 'r_-19': 4, 'r_-3': 4, 'l_-8': 115016248, 'r_-12': 78578125, 'c_1': 0, 'l_3': 4915261, 'l_-6': 3, 'r_-8': 115016248, 'r_-11': 4915261, 'l_-3': 4, 'r_-20': 3, 'r_-9': 5, 'l_2': 4, 'l_-1': 4, 'r_-14': 48628067, 'r_-6': 3, 'r_-16': 4, 'r_-10': 3, 'r_-13': 4915261, 'r_-15': 4915261, 'r_-2': 3, 'l_1': 4259891, 'l_4': 48628067, 'l_7': 4915261, 'r_-5': 4, 'l_-2': 3, 'l_6': 78578125, 'l_8': 3, 'r_-7': 4}},
        {'text_pos': 692, 'atts': {'r_-19': 4915261, 'r_-1': 4915261, 'l_-7': 4259891, 'r_-13': 4, 'l_-12': 3, 'r_-4': 48628067, 'l_-5': 4915261, 'l_-14': 3, 'r_-17': 5, 'c_-1': 5, 'r_-18': 3, 'l_-4': 48628067, 'r_-3': 4915261, 'l_-15': 4, 'l_-8': 3, 'r_-12': 3, 'c_1': 0, 'l_-13': 4, 'l_-6': 4, 'l_-2': 78578125, 'r_-8': 3, 'r_-11': 4, 'l_-3': 4915261, 'l_-11': 4, 'r_-20': 78578125, 'l_-9': 4, 'l_-1': 4915261, 'r_-14': 3, 'r_-9': 4, 'r_-16': 115016248, 'r_-10': 3, 'r_-15': 4, 'l_-10': 3, 'r_-6': 4, 'r_-2': 78578125, 'l_1': 5, 'r_-5': 4915261, 'l_-16': 115016248, 'r_-7': 4259891}}]
        hashed_text=varapi.get_hashed_text(text)
        var_atts2=varapi.get_variables_atts(hashed_text)
        self.assertEqual(var_atts, var_atts2)


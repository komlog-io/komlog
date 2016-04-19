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
        text='MemTotal:        3085780 kB\nMemFree:          835216 kB\nMemAvailable:    1509660 kB\nBuffers:          304576 kB\nCached:           304132 kB\nSwapCached:            0 kB\nActive:           734184 kB\nInactive:         155608 kB\nActive(anon):     304772 kB\nInactive(anon):      344 kB\nActive(file):     429412 kB\nInactive(file):   155264 kB\nUnevictable:     1192276 kB\nMlocked:         1192276 kB\nSwapTotal:             0 kB\nSwapFree:              0 kB\nDirty:               344 kB\nWriteback:             0 kB\nAnonPages:       1382500 kB\nMapped:            58880 kB\nShmem:              1184 kB\nSlab:             142336 kB\nSReclaimable:     129504 kB\nSUnreclaim:        12832 kB\nKernelStack:        2784 kB\nPageTables:         7672 kB\nNFS_Unstable:          0 kB\nBounce:                0 kB\nWritebackTmp:          0 kB\nCommitLimit:     1542888 kB\nCommitted_AS:    1548912 kB\nVmallocTotal:   34359738367 kB\nVmallocUsed:           0 kB\nVmallocChunk:          0 kB\nHardwareCorrupted:     0 kB\nAnonHugePages:   1255424 kB\nHugePages_Total:       0\nHugePages_Free:        0\nHugePages_Rsvd:        0\nHugePages_Surp:        0\nHugepagesize:       2048 kB\nDirectMap4k:       44992 kB\nDirectMap2M:     3100672 kB\n'
        hashed_text={'elements': [
            {'text_pos': 0, 'hash': 237044529, 'line_pos': 0, 'length': 8, 'line': 1, 'order': 1},
            {'text_pos': 8, 'hash': 5636168, 'line_pos': 8, 'length': 1, 'line': 1, 'order': 2},
            {'text_pos': 9, 'hash': 4, 'line_pos': 9, 'length': 8, 'line': 1, 'order': 3},
            {'type': 'var', 'text_pos': 17, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '3085780', 'decsep': 'n', 'line': 1, 'order': 4},
            {'text_pos': 24, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 1, 'order': 5},
            {'text_pos': 25, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 1, 'order': 6},
            {'text_pos': 27, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 1, 'order': 7},
            {'text_pos': 28, 'hash': 178717359, 'line_pos': 0, 'length': 7, 'line': 2, 'order': 8},
            {'text_pos': 35, 'hash': 5636168, 'line_pos': 7, 'length': 1, 'line': 2, 'order': 9},
            {'text_pos': 36, 'hash': 4, 'line_pos': 8, 'length': 10, 'line': 2, 'order': 10},
            {'type': 'var', 'text_pos': 46, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '835216', 'decsep': 'n', 'line': 2, 'order': 11},
            {'text_pos': 52, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 2, 'order': 12},
            {'text_pos': 53, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 2, 'order': 13},
            {'text_pos': 55, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 2, 'order': 14},
            {'text_pos': 56, 'hash': 503579822, 'line_pos': 0, 'length': 12, 'line': 3, 'order': 15},
            {'text_pos': 68, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 3, 'order': 16},
            {'text_pos': 69, 'hash': 4, 'line_pos': 13, 'length': 4, 'line': 3, 'order': 17},
            {'type': 'var', 'text_pos': 73, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1509660', 'decsep': 'n', 'line': 3, 'order': 18},
            {'text_pos': 80, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 3, 'order': 19},
            {'text_pos': 81, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 3, 'order': 20},
            {'text_pos': 83, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 3, 'order': 21},
            {'text_pos': 84, 'hash': 186122971, 'line_pos': 0, 'length': 7, 'line': 4, 'order': 22},
            {'text_pos': 91, 'hash': 5636168, 'line_pos': 7, 'length': 1, 'line': 4, 'order': 23},
            {'text_pos': 92, 'hash': 4, 'line_pos': 8, 'length': 10, 'line': 4, 'order': 24},
            {'type': 'var', 'text_pos': 102, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '304576', 'decsep': 'n', 'line': 4, 'order': 25},
            {'text_pos': 108, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 4, 'order': 26},
            {'text_pos': 109, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 4, 'order': 27},
            {'text_pos': 111, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 4, 'order': 28},
            {'text_pos': 112, 'hash': 130744902, 'line_pos': 0, 'length': 6, 'line': 5, 'order': 29},
            {'text_pos': 118, 'hash': 5636168, 'line_pos': 6, 'length': 1, 'line': 5, 'order': 30},
            {'text_pos': 119, 'hash': 4, 'line_pos': 7, 'length': 11, 'line': 5, 'order': 31},
            {'type': 'var', 'text_pos': 130, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '304132', 'decsep': 'n', 'line': 5, 'order': 32},
            {'text_pos': 136, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 5, 'order': 33},
            {'text_pos': 137, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 5, 'order': 34},
            {'text_pos': 139, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 5, 'order': 35},
            {'text_pos': 140, 'hash': 361235425, 'line_pos': 0, 'length': 10, 'line': 6, 'order': 36},
            {'text_pos': 150, 'hash': 5636168, 'line_pos': 10, 'length': 1, 'line': 6, 'order': 37},
            {'text_pos': 151, 'hash': 4, 'line_pos': 11, 'length': 12, 'line': 6, 'order': 38},
            {'type': 'var', 'text_pos': 163, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 6, 'order': 39},
            {'text_pos': 164, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 6, 'order': 40},
            {'text_pos': 165, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 6, 'order': 41},
            {'text_pos': 167, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 6, 'order': 42},
            {'text_pos': 168, 'hash': 137560682, 'line_pos': 0, 'length': 6, 'line': 7, 'order': 43},
            {'text_pos': 174, 'hash': 5636168, 'line_pos': 6, 'length': 1, 'line': 7, 'order': 44},
            {'text_pos': 175, 'hash': 4, 'line_pos': 7, 'length': 11, 'line': 7, 'order': 45},
            {'type': 'var', 'text_pos': 186, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '734184', 'decsep': 'n', 'line': 7, 'order': 46},
            {'text_pos': 192, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 7, 'order': 47},
            {'text_pos': 193, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 7, 'order': 48},
            {'text_pos': 195, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 7, 'order': 49},
            {'text_pos': 196, 'hash': 240714561, 'line_pos': 0, 'length': 8, 'line': 8, 'order': 50},
            {'text_pos': 204, 'hash': 5636168, 'line_pos': 8, 'length': 1, 'line': 8, 'order': 51},
            {'text_pos': 205, 'hash': 4, 'line_pos': 9, 'length': 9, 'line': 8, 'order': 52},
            {'type': 'var', 'text_pos': 214, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '155608', 'decsep': 'n', 'line': 8, 'order': 53},
            {'text_pos': 220, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 8, 'order': 54},
            {'text_pos': 221, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 8, 'order': 55},
            {'text_pos': 223, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 8, 'order': 56},
            {'text_pos': 224, 'hash': 137560682, 'line_pos': 0, 'length': 6, 'line': 9, 'order': 57},
            {'text_pos': 230, 'hash': 4456502, 'line_pos': 6, 'length': 1, 'line': 9, 'order': 58},
            {'text_pos': 231, 'hash': 73400762, 'line_pos': 7, 'length': 4, 'line': 9, 'order': 59},
            {'text_pos': 235, 'hash': 4522039, 'line_pos': 11, 'length': 1, 'line': 9, 'order': 60},
            {'text_pos': 236, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 9, 'order': 61},
            {'text_pos': 237, 'hash': 4, 'line_pos': 13, 'length': 5, 'line': 9, 'order': 62},
            {'type': 'var', 'text_pos': 242, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '304772', 'decsep': 'n', 'line': 9, 'order': 63},
            {'text_pos': 248, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 9, 'order': 64},
            {'text_pos': 249, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 9, 'order': 65},
            {'text_pos': 251, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 9, 'order': 66},
            {'text_pos': 252, 'hash': 240714561, 'line_pos': 0, 'length': 8, 'line': 10, 'order': 67},
            {'text_pos': 260, 'hash': 4456502, 'line_pos': 8, 'length': 1, 'line': 10, 'order': 68},
            {'text_pos': 261, 'hash': 73400762, 'line_pos': 9, 'length': 4, 'line': 10, 'order': 69},
            {'text_pos': 265, 'hash': 4522039, 'line_pos': 13, 'length': 1, 'line': 10, 'order': 70},
            {'text_pos': 266, 'hash': 5636168, 'line_pos': 14, 'length': 1, 'line': 10, 'order': 71},
            {'text_pos': 267, 'hash': 4, 'line_pos': 15, 'length': 6, 'line': 10, 'order': 72},
            {'type': 'var', 'text_pos': 273, 'length': 3, 'hash': 3, 'line_pos': 21, 'content': '344', 'decsep': 'n', 'line': 10, 'order': 73},
            {'text_pos': 276, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 10, 'order': 74},
            {'text_pos': 277, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 10, 'order': 75},
            {'text_pos': 279, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 10, 'order': 76},
            {'text_pos': 280, 'hash': 137560682, 'line_pos': 0, 'length': 6, 'line': 11, 'order': 77},
            {'text_pos': 286, 'hash': 4456502, 'line_pos': 6, 'length': 1, 'line': 11, 'order': 78},
            {'text_pos': 287, 'hash': 72745390, 'line_pos': 7, 'length': 4, 'line': 11, 'order': 79},
            {'text_pos': 291, 'hash': 4522039, 'line_pos': 11, 'length': 1, 'line': 11, 'order': 80},
            {'text_pos': 292, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 11, 'order': 81},
            {'text_pos': 293, 'hash': 4, 'line_pos': 13, 'length': 5, 'line': 11, 'order': 82},
            {'type': 'var', 'text_pos': 298, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '429412', 'decsep': 'n', 'line': 11, 'order': 83},
           
            {'text_pos': 304, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 11, 'order': 84},
            {'text_pos': 305, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 11, 'order': 85},
            {'text_pos': 307, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 11, 'order': 86},
            {'text_pos': 308, 'hash': 240714561, 'line_pos': 0, 'length': 8, 'line': 12, 'order': 87},
            {'text_pos': 316, 'hash': 4456502, 'line_pos': 8, 'length': 1, 'line': 12, 'order': 88},
            {'text_pos': 317, 'hash': 72745390, 'line_pos': 9, 'length': 4, 'line': 12, 'order': 89},
            {'text_pos': 321, 'hash': 4522039, 'line_pos': 13, 'length': 1, 'line': 12, 'order': 90},
            {'text_pos': 322, 'hash': 5636168, 'line_pos': 14, 'length': 1, 'line': 12, 'order': 91},
            {'text_pos': 323, 'hash': 4, 'line_pos': 15, 'length': 3, 'line': 12, 'order': 92},
            {'type': 'var', 'text_pos': 326, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '155264', 'decsep': 'n', 'line': 12, 'order': 93},
            {'text_pos': 332, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 12, 'order': 94},
            {'text_pos': 333, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 12, 'order': 95},
            {'text_pos': 335, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 12, 'order': 96},
            {'text_pos': 336, 'hash': 456393856, 'line_pos': 0, 'length': 11, 'line': 13, 'order': 97},
            {'text_pos': 347, 'hash': 5636168, 'line_pos': 11, 'length': 1, 'line': 13, 'order': 98},
            {'text_pos': 348, 'hash': 4, 'line_pos': 12, 'length': 5, 'line': 13, 'order': 99},
            {'type': 'var', 'text_pos': 353, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1192276', 'decsep': 'n', 'line': 13, 'order': 100},
            {'text_pos': 360, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 13, 'order': 101},
            {'text_pos': 361, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 13, 'order': 102},
            {'text_pos': 363, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 13, 'order': 103},
            {'text_pos': 364, 'hash': 188285645, 'line_pos': 0, 'length': 7, 'line': 14, 'order': 104},
            {'text_pos': 371, 'hash': 5636168, 'line_pos': 7, 'length': 1, 'line': 14, 'order': 105},
            {'text_pos': 372, 'hash': 4, 'line_pos': 8, 'length': 9, 'line': 14, 'order': 106},
            {'type': 'var', 'text_pos': 381, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1192276', 'decsep': 'n', 'line': 14, 'order': 107},
            {'text_pos': 388, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 14, 'order': 108},
            {'text_pos': 389, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 14, 'order': 109},
            {'text_pos': 391, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 14, 'order': 110},
            {'text_pos': 392, 'hash': 308282285, 'line_pos': 0, 'length': 9, 'line': 15, 'order': 111},
            {'text_pos': 401, 'hash': 5636168, 'line_pos': 9, 'length': 1, 'line': 15, 'order': 112},
            {'text_pos': 402, 'hash': 4, 'line_pos': 10, 'length': 13, 'line': 15, 'order': 113},
            {'type': 'var', 'text_pos': 415, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 15, 'order': 114},
            {'text_pos': 416, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 15, 'order': 115},
            {'text_pos': 417, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 15, 'order': 116},
            {'text_pos': 419, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 15, 'order': 117},
            {'text_pos': 420, 'hash': 241828651, 'line_pos': 0, 'length': 8, 'line': 16, 'order': 118},
            {'text_pos': 428, 'hash': 5636168, 'line_pos': 8, 'length': 1, 'line': 16, 'order': 119},
            {'text_pos': 429, 'hash': 4, 'line_pos': 9, 'length': 14, 'line': 16, 'order': 120},
            {'type': 'var', 'text_pos': 443, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 16, 'order': 121},
            {'text_pos': 444, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 16, 'order': 122},
            {'text_pos': 445, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 16, 'order': 123},
            {'text_pos': 447, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 16, 'order': 124},
            {'text_pos': 448, 'hash': 100860442, 'line_pos': 0, 'length': 5, 'line': 17, 'order': 125},
            {'text_pos': 453, 'hash': 5636168, 'line_pos': 5, 'length': 1, 'line': 17, 'order': 126},
            {'text_pos': 454, 'hash': 4, 'line_pos': 6, 'length': 15, 'line': 17, 'order': 127},
            {'type': 'var', 'text_pos': 469, 'length': 3, 'hash': 3, 'line_pos': 21, 'content': '344', 'decsep': 'n', 'line': 17, 'order': 128},
            {'text_pos': 472, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 17, 'order': 129},
            {'text_pos': 473, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 17, 'order': 130},
            {'text_pos': 475, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 17, 'order': 131},
            {'text_pos': 476, 'hash': 311886762, 'line_pos': 0, 'length': 9, 'line': 18, 'order': 132},
            {'text_pos': 485, 'hash': 5636168, 'line_pos': 9, 'length': 1, 'line': 18, 'order': 133},
            {'text_pos': 486, 'hash': 4, 'line_pos': 10, 'length': 13, 'line': 18, 'order': 134},
            {'type': 'var', 'text_pos': 499, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 18, 'order': 135},
            {'text_pos': 500, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 18, 'order': 136},
            {'text_pos': 501, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 18, 'order': 137},
            {'text_pos': 503, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 18, 'order': 138},
            {'text_pos': 504, 'hash': 292029322, 'line_pos': 0, 'length': 9, 'line': 19, 'order': 139},
            {'text_pos': 513, 'hash': 5636168, 'line_pos': 9, 'length': 1, 'line': 19, 'order': 140},
            {'text_pos': 514, 'hash': 4, 'line_pos': 10, 'length': 7, 'line': 19, 'order': 141},
            {'type': 'var', 'text_pos': 521, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1382500', 'decsep': 'n', 'line': 19, 'order': 142},
            {'text_pos': 528, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 19, 'order': 143},
            {'text_pos': 529, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 19, 'order': 144},
            {'text_pos': 531, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 19, 'order': 145},
            {'text_pos': 532, 'hash': 139657829, 'line_pos': 0, 'length': 6, 'line': 20, 'order': 146},
            {'text_pos': 538, 'hash': 5636168, 'line_pos': 6, 'length': 1, 'line': 20, 'order': 147},
            {'text_pos': 539, 'hash': 4, 'line_pos': 7, 'length': 12, 'line': 20, 'order': 148},
            {'type': 'var', 'text_pos': 551, 'length': 5, 'hash': 3, 'line_pos': 19, 'content': '58880', 'decsep': 'n', 'line': 20, 'order': 149},
            {'text_pos': 556, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 20, 'order': 150},
            {'text_pos': 557, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 20, 'order': 151},
            {'text_pos': 559, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 20, 'order': 152},
            {'text_pos': 560, 'hash': 101777928, 'line_pos': 0, 'length': 5, 'line': 21, 'order': 153},
            {'text_pos': 565, 'hash': 5636168, 'line_pos': 5, 'length': 1, 'line': 21, 'order': 154},
            {'text_pos': 566, 'hash': 4, 'line_pos': 6, 'length': 14, 'line': 21, 'order': 155},
            {'type': 'var', 'text_pos': 580, 'length': 4, 'hash': 3, 'line_pos': 20, 'content': '1184', 'decsep': 'n', 'line': 21, 'order': 156},
            {'text_pos': 584, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 21, 'order': 157},
            {'text_pos': 585, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 21, 'order': 158},
            {'text_pos': 587, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 21, 'order': 159},
            {'text_pos': 588, 'hash': 66716048, 'line_pos': 0, 'length': 4, 'line': 22, 'order': 160},
            {'text_pos': 592, 'hash': 5636168, 'line_pos': 4, 'length': 1, 'line': 22, 'order': 161},
            {'text_pos': 593, 'hash': 4, 'line_pos': 5, 'length': 13, 'line': 22, 'order': 162},
            {'type': 'var', 'text_pos': 606, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '142336', 'decsep': 'n', 'line': 22, 'order': 163},
            {'text_pos': 612, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 22, 'order': 164},
            {'text_pos': 613, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 22, 'order': 165},
            {'text_pos': 615, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 22, 'order': 166},
            {'text_pos': 616, 'hash': 504497330, 'line_pos': 0, 'length': 12, 'line': 23, 'order': 167},
            {'text_pos': 628, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 23, 'order': 168},
            {'text_pos': 629, 'hash': 4, 'line_pos': 13, 'length': 5, 'line': 23, 'order': 169},
            {'type': 'var', 'text_pos': 634, 'length': 6, 'hash': 3, 'line_pos': 18, 'content': '129504', 'decsep': 'n', 'line': 23, 'order': 170},
            {'text_pos': 640, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 23, 'order': 171},
            {'text_pos': 641, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 23, 'order': 172},
            {'text_pos': 643, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 23, 'order': 173},
            {'text_pos': 644, 'hash': 365036545, 'line_pos': 0, 'length': 10, 'line': 24, 'order': 174},
            {'text_pos': 654, 'hash': 5636168, 'line_pos': 10, 'length': 1, 'line': 24, 'order': 175},
            {'text_pos': 655, 'hash': 4, 'line_pos': 11, 'length': 8, 'line': 24, 'order': 176},
            {'type': 'var', 'text_pos': 663, 'length': 5, 'hash': 3, 'line_pos': 19, 'content': '12832', 'decsep': 'n', 'line': 24, 'order': 177},
            {'text_pos': 668, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 24, 'order': 178},
            {'text_pos': 669, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 24, 'order': 179},
            {'text_pos': 671, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 24, 'order': 180},
            {'text_pos': 672, 'hash': 441648229, 'line_pos': 0, 'length': 11, 'line': 25, 'order': 181},
            {'text_pos': 683, 'hash': 5636168, 'line_pos': 11, 'length': 1, 'line': 25, 'order': 182},
            {'text_pos': 684, 'hash': 4, 'line_pos': 12, 'length': 8, 'line': 25, 'order': 183},
            {'type': 'var', 'text_pos': 692, 'length': 4, 'hash': 3, 'line_pos': 20, 'content': '2784', 'decsep': 'n', 'line': 25, 'order': 184},
            {'text_pos': 696, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 25, 'order': 185},
            {'text_pos': 697, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 25, 'order': 186},
            {'text_pos': 699, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 25, 'order': 187},
            {'text_pos': 700, 'hash': 352584678, 'line_pos': 0, 'length': 10, 'line': 26, 'order': 188},
            {'text_pos': 710, 'hash': 5636168, 'line_pos': 10, 'length': 1, 'line': 26, 'order': 189},
            {'text_pos': 711, 'hash': 4, 'line_pos': 11, 'length': 9, 'line': 26, 'order': 190},
            {'type': 'var', 'text_pos': 720, 'length': 4, 'hash': 3, 'line_pos': 20, 'content': '7672', 'decsep': 'n', 'line': 26, 'order': 191},
            {'text_pos': 724, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 26, 'order': 192},
            {'text_pos': 725, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 26, 'order': 193},
            {'text_pos': 727, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 26, 'order': 194},
            {'text_pos': 728, 'hash': 477889682, 'line_pos': 0, 'length': 12, 'line': 27, 'order': 195},
            {'text_pos': 740, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 27, 'order': 196},
            {'text_pos': 741, 'hash': 4, 'line_pos': 13, 'length': 10, 'line': 27, 'order': 197},
            {'type': 'var', 'text_pos': 751, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 27, 'order': 198},
            {'text_pos': 752, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 27, 'order': 199},
            {'text_pos': 753, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 27, 'order': 200},
            {'text_pos': 755, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 27, 'order': 201},
            {'text_pos': 756, 'hash': 140640874, 'line_pos': 0, 'length': 6, 'line': 28, 'order': 202},
            {'text_pos': 762, 'hash': 5636168, 'line_pos': 6, 'length': 1, 'line': 28, 'order': 203},
            {'text_pos': 763, 'hash': 4, 'line_pos': 7, 'length': 16, 'line': 28, 'order': 204},
            {'type': 'var', 'text_pos': 779, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 28, 'order': 205},
            {'text_pos': 780, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 28, 'order': 206},
            {'text_pos': 781, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 28, 'order': 207},
            {'text_pos': 783, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 28, 'order': 208},
            {'text_pos': 784, 'hash': 534447323, 'line_pos': 0, 'length': 12, 'line': 29, 'order': 209},
            {'text_pos': 796, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 29, 'order': 210},
            {'text_pos': 797, 'hash': 4, 'line_pos': 13, 'length': 10, 'line': 29, 'order': 211},
            {'type': 'var', 'text_pos': 807, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 29, 'order': 212},
            {'text_pos': 808, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 29, 'order': 213},
            {'text_pos': 809, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 29, 'order': 214},
            {'text_pos': 811, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 29, 'order': 215},
            {'text_pos': 812, 'hash': 442500214, 'line_pos': 0, 'length': 11, 'line': 30, 'order': 216},
            {'text_pos': 823, 'hash': 5636168, 'line_pos': 11, 'length': 1, 'line': 30, 'order': 217},
            {'text_pos': 824, 'hash': 4, 'line_pos': 12, 'length': 5, 'line': 30, 'order': 218},
            {'type': 'var', 'text_pos': 829, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1542888', 'decsep': 'n', 'line': 30, 'order': 219},
            {'text_pos': 836, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 30, 'order': 220},
            {'text_pos': 837, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 30, 'order': 221},
            {'text_pos': 839, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 30, 'order': 222},
            {'text_pos': 840, 'hash': 526189735, 'line_pos': 0, 'length': 12, 'line': 31, 'order': 223},
            {'text_pos': 852, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 31, 'order': 224},
            {'text_pos': 853, 'hash': 4, 'line_pos': 13, 'length': 4, 'line': 31, 'order': 225},
            {'type': 'var', 'text_pos': 857, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1548912', 'decsep': 'n', 'line': 31, 'order': 226},
            {'text_pos': 864, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 31, 'order': 227},
            {'text_pos': 865, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 31, 'order': 228},
            {'text_pos': 867, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 31, 'order': 229},
            {'text_pos': 868, 'hash': 531104992, 'line_pos': 0, 'length': 12, 'line': 32, 'order': 230},
            {'text_pos': 880, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 32, 'order': 231},
            {'text_pos': 881, 'hash': 4, 'line_pos': 13, 'length': 3, 'line': 32, 'order': 232},
            {'type': 'var', 'text_pos': 884, 'length': 11, 'hash': 3, 'line_pos': 16, 'content': '34359738367', 'decsep': 'n', 'line': 32, 'order': 233},
            {'text_pos': 895, 'hash': 4, 'line_pos': 27, 'length': 1, 'line': 32, 'order': 234},
            {'text_pos': 896, 'hash': 21102779, 'line_pos': 28, 'length': 2, 'line': 32, 'order': 235},
            {'text_pos': 898, 'hash': 5, 'line_pos': 30, 'length': 1, 'line': 32, 'order': 236},
            {'text_pos': 899, 'hash': 448595053, 'line_pos': 0, 'length': 11, 'line': 33, 'order': 237},
            {'text_pos': 910, 'hash': 5636168, 'line_pos': 11, 'length': 1, 'line': 33, 'order': 238},
            {'text_pos': 911, 'hash': 4, 'line_pos': 12, 'length': 11, 'line': 33, 'order': 239},
            {'type': 'var', 'text_pos': 922, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 33, 'order': 240},
            {'text_pos': 923, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 33, 'order': 241},
            {'text_pos': 924, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 33, 'order': 242},
            {'text_pos': 926, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 33, 'order': 243},
            {'text_pos': 927, 'hash': 525534421, 'line_pos': 0, 'length': 12, 'line': 34, 'order': 244},
            {'text_pos': 939, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 34, 'order': 245},
            {'text_pos': 940, 'hash': 4, 'line_pos': 13, 'length': 10, 'line': 34, 'order': 246},
            {'type': 'var', 'text_pos': 950, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 34, 'order': 247},
            {'text_pos': 951, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 34, 'order': 248},
            {'text_pos': 952, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 34, 'order': 249},
            {'text_pos': 954, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 34, 'order': 250},
            {'text_pos': 955, 'hash': 1033438964, 'line_pos': 0, 'length': 17, 'line': 35, 'order': 251},
            {'text_pos': 972, 'hash': 5636168, 'line_pos': 17, 'length': 1, 'line': 35, 'order': 252},
            {'text_pos': 973, 'hash': 4, 'line_pos': 18, 'length': 5, 'line': 35, 'order': 253},
            {'type': 'var', 'text_pos': 978, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 35, 'order': 254},
            {'text_pos': 979, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 35, 'order': 255},
            {'text_pos': 980, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 35, 'order': 256},
            {'text_pos': 982, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 35, 'order': 257},
            {'text_pos': 983, 'hash': 590284051, 'line_pos': 0, 'length': 13, 'line': 36, 'order': 258},
            {'text_pos': 996, 'hash': 5636168, 'line_pos': 13, 'length': 1, 'line': 36, 'order': 259},
            {'text_pos': 997, 'hash': 4, 'line_pos': 14, 'length': 3, 'line': 36, 'order': 260},
            {'type': 'var', 'text_pos': 1000, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '1255424', 'decsep': 'n', 'line': 36, 'order': 261},
            {'text_pos': 1007, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 36, 'order': 262},
            {'text_pos': 1008, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 36, 'order': 263},
            {'text_pos': 1010, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 36, 'order': 264},
            {'text_pos': 1011, 'hash': 784270826, 'line_pos': 0, 'length': 15, 'line': 37, 'order': 265},
            {'text_pos': 1026, 'hash': 5636168, 'line_pos': 15, 'length': 1, 'line': 37, 'order': 266},
            {'text_pos': 1027, 'hash': 4, 'line_pos': 16, 'length': 7, 'line': 37, 'order': 267},
            {'type': 'var', 'text_pos': 1034, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 37, 'order': 268},
            {'text_pos': 1035, 'hash': 5, 'line_pos': 24, 'length': 1, 'line': 37, 'order': 269},
            {'text_pos': 1036, 'hash': 680265064, 'line_pos': 0, 'length': 14, 'line': 38, 'order': 270},
            {'text_pos': 1050, 'hash': 5636168, 'line_pos': 14, 'length': 1, 'line': 38, 'order': 271},
            {'text_pos': 1051, 'hash': 4, 'line_pos': 15, 'length': 8, 'line': 38, 'order': 272},
            {'type': 'var', 'text_pos': 1059, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 38, 'order': 273},
            {'text_pos': 1060, 'hash': 5, 'line_pos': 24, 'length': 1, 'line': 38, 'order': 274},
            {'text_pos': 1061, 'hash': 685770117, 'line_pos': 0, 'length': 14, 'line': 39, 'order': 275},
            {'text_pos': 1075, 'hash': 5636168, 'line_pos': 14, 'length': 1, 'line': 39, 'order': 276},
            {'text_pos': 1076, 'hash': 4, 'line_pos': 15, 'length': 8, 'line': 39, 'order': 277},
            {'type': 'var', 'text_pos': 1084, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 39, 'order': 278},
            {'text_pos': 1085, 'hash': 5, 'line_pos': 24, 'length': 1, 'line': 39, 'order': 279},
            {'text_pos': 1086, 'hash': 686687632, 'line_pos': 0, 'length': 14, 'line': 40, 'order': 280},
            {'text_pos': 1100, 'hash': 5636168, 'line_pos': 14, 'length': 1, 'line': 40, 'order': 281},
            {'text_pos': 1101, 'hash': 4, 'line_pos': 15, 'length': 8, 'line': 40, 'order': 282},
            {'type': 'var', 'text_pos': 1109, 'length': 1, 'hash': 3, 'line_pos': 23, 'content': '0', 'decsep': 'n', 'line': 40, 'order': 283},
            {'text_pos': 1110, 'hash': 5, 'line_pos': 24, 'length': 1, 'line': 40, 'order': 284},
            {'text_pos': 1111, 'hash': 530187503, 'line_pos': 0, 'length': 12, 'line': 41, 'order': 285},
            {'text_pos': 1123, 'hash': 5636168, 'line_pos': 12, 'length': 1, 'line': 41, 'order': 286},
            {'text_pos': 1124, 'hash': 4, 'line_pos': 13, 'length': 7, 'line': 41, 'order': 287},
            {'type': 'var', 'text_pos': 1131, 'length': 4, 'hash': 3, 'line_pos': 20, 'content': '2048', 'decsep': 'n', 'line': 41, 'order': 288},
            {'text_pos': 1135, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 41, 'order': 289},
            {'text_pos': 1136, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 41, 'order': 290},
            {'text_pos': 1138, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 41, 'order': 291},
            {'text_pos': 1139, 'hash': 426574886, 'line_pos': 0, 'length': 11, 'line': 42, 'order': 292},
            {'text_pos': 1150, 'hash': 5636168, 'line_pos': 11, 'length': 1, 'line': 42, 'order': 293},
            {'text_pos': 1151, 'hash': 4, 'line_pos': 12, 'length': 7, 'line': 42, 'order': 294},
            {'type': 'var', 'text_pos': 1158, 'length': 5, 'hash': 3, 'line_pos': 19, 'content': '44992', 'decsep': 'n', 'line': 42, 'order': 295},
            {'text_pos': 1163, 'hash': 4, 'line_pos': 24, 'length': 1, 'line': 42, 'order': 296},
            {'text_pos': 1164, 'hash': 21102779, 'line_pos': 25, 'length': 2, 'line': 42, 'order': 297},
            {'text_pos': 1166, 'hash': 5, 'line_pos': 27, 'length': 1, 'line': 42, 'order': 298},
            {'text_pos': 1167, 'hash': 424346630, 'line_pos': 0, 'length': 11, 'line': 43, 'order': 299},
            {'text_pos': 1178, 'hash': 5636168, 'line_pos': 11, 'length': 1, 'line': 43, 'order': 300},
            {'text_pos': 1179, 'hash': 4, 'line_pos': 12, 'length': 5, 'line': 43, 'order': 301},
            {'type': 'var', 'text_pos': 1184, 'length': 7, 'hash': 3, 'line_pos': 17, 'content': '3100672', 'decsep': 'n', 'line': 43, 'order': 302}],
        'header_lines': []}
        hashed_text2=varapi.get_hashed_text(text)
        self.assertTrue('elements' in hashed_text2)
        self.assertTrue('header_lines' in hashed_text2)
        self.assertEqual(hashed_text2['header_lines'],hashed_text['header_lines'])
        self.assertEqual(len(hashed_text2['elements']),len(hashed_text['elements']))
        self.assertEqual(hashed_text2['elements'],hashed_text['elements'])

    def test_get_variables_atts_success(self):
        ''' get_variables_atts should return the attributes associated to every text variable to identify uniquely in the text '''
        var_atts=[
        {'text_pos': 17, 'atts': {'c_1': 0, 'c_-1': 0, 'l_2': 21102779, 'l_-2': 5636168, 'l_3': 5, 'l_-1': 4, 'r_-2': 5636168, 'l_-3': 237044529, 'r_-1': 4, 'r_-3': 237044529, 'l_1': 4, 'r_-4': 1}},
        {'text_pos': 46, 'atts': {'c_1': 0, 'l_3': 5, 'l_2': 21102779, 'r_-11': 1, 'r_-6': 4, 'r_-5': 21102779, 'r_-7': 3, 'r_-10': 237044529, 'r_-2': 5636168, 'c_-1': 0, 'l_-1': 4, 'r_-3': 178717359, 'r_-9': 5636168, 'r_-8': 4, 'l_-2': 5636168, 'l_1': 4, 'r_-4': 5, 'r_-1': 4, 'l_-3': 178717359}},
        {'text_pos': 73, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 237044529, 'r_-12': 21102779, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-3': 503579822, 'l_-1': 4, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 178717359, 'r_-13': 4, 'r_-18': 1, 'l_-3': 503579822, 'r_-8': 4, 'r_-14': 3, 'r_-4': 5}},
        {'text_pos': 102, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 178717359, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 186122971, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 503579822, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 186122971}},
        {'text_pos': 130, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 503579822, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 130744902, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 186122971, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 130744902}},
        {'text_pos': 163, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 186122971, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 361235425, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 130744902, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 361235425}},
        {'text_pos': 186, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 130744902, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 137560682, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 361235425, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 137560682}},
        {'text_pos': 214, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 361235425, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 240714561, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 137560682, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 240714561}},
        {'text_pos': 242, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-8': 21102779, 'r_-5': 4456502, 'r_-7': 5, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 3, 'r_-12': 5636168, 'r_-9': 4, 'l_-4': 73400762, 'r_-11': 4, 'l_1': 4, 'r_-15': 21102779, 'r_-1': 4, 'r_-20': 137560682, 'r_-3': 4522039, 'l_-1': 4, 'r_-16': 4, 'c_1': 0, 'r_-6': 137560682, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 240714561, 'r_-18': 4, 'l_-5': 4456502, 'r_-4': 73400762, 'r_-19': 5636168, 'l_-6': 137560682, 'r_-14': 5, 'l_-3': 4522039}},
        {'text_pos': 273, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-8': 21102779, 'r_-5': 4456502, 'r_-7': 5, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 5, 'r_-12': 5636168, 'r_-9': 4, 'l_-4': 73400762, 'r_-11': 4, 'l_1': 4, 'r_-15': 4456502, 'r_-1': 4, 'r_-20': 3, 'r_-3': 4522039, 'l_-1': 4, 'r_-16': 137560682, 'c_1': 0, 'r_-6': 240714561, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 4522039, 'r_-18': 21102779, 'l_-5': 4456502, 'r_-4': 73400762, 'r_-19': 4, 'l_-6': 240714561, 'r_-14': 73400762, 'l_-3': 4522039}},
        {'text_pos': 298, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-8': 21102779, 'r_-5': 4456502, 'r_-7': 5, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 5, 'r_-12': 5636168, 'r_-9': 4, 'l_-4': 72745390, 'r_-11': 4, 'l_1': 4, 'r_-15': 4456502, 'r_-1': 4, 'r_-20': 3, 'r_-3': 4522039, 'l_-1': 4, 'r_-16': 240714561, 'c_1': 0, 'r_-6': 137560682, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 4522039, 'r_-18': 21102779, 'l_-5': 4456502, 'r_-4': 72745390, 'r_-19': 4, 'l_-6': 137560682, 'r_-14': 73400762, 'l_-3': 4522039}},
        {'text_pos': 326, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-8': 21102779, 'r_-5': 4456502, 'r_-7': 5, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 5, 'r_-12': 5636168, 'r_-9': 4, 'l_-4': 72745390, 'r_-11': 4, 'l_1': 4, 'r_-15': 4456502, 'r_-1': 4, 'r_-20': 3, 'r_-3': 4522039, 'l_-1': 4, 'r_-16': 137560682, 'c_1': 0, 'r_-6': 240714561, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 4522039, 'r_-18': 21102779, 'l_-5': 4456502, 'r_-4': 72745390, 'r_-19': 4, 'l_-6': 240714561, 'r_-14': 72745390, 'l_-3': 4522039}},
        {'text_pos': 353, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 5636168, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 3, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 72745390, 'l_1': 4, 'r_-15': 21102779, 'r_-1': 4, 'r_-20': 4522039, 'r_-3': 456393856, 'r_-12': 4456502, 'r_-16': 4, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 4522039, 'r_-13': 240714561, 'r_-18': 4, 'r_-4': 5, 'r_-8': 4, 'r_-14': 5, 'l_-3': 456393856}},
        {'text_pos': 381, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 4456502, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 4522039, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 240714561, 'r_-3': 188285645, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 456393856, 'r_-13': 4, 'r_-18': 72745390, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 188285645}},
        {'text_pos': 415, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 456393856, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 308282285, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 188285645, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 308282285}},
        {'text_pos': 443, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 188285645, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 241828651, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 308282285, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 241828651}},
        {'text_pos': 469, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 308282285, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 100860442, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 241828651, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 100860442}},
        {'text_pos': 499, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 241828651, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 311886762, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 100860442, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 311886762}},
        {'text_pos': 521, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 100860442, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 292029322, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 311886762, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 292029322}},
        {'text_pos': 551, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 311886762, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 139657829, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 292029322, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 139657829}},
        {'text_pos': 580, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 292029322, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 101777928, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 139657829, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 101777928}},
        {'text_pos': 606, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 139657829, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 66716048, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 101777928, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 66716048}},
        {'text_pos': 634, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 101777928, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 504497330, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 66716048, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 504497330}},
        {'text_pos': 663, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 66716048, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 365036545, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 504497330, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 365036545}},
        {'text_pos': 692, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 504497330, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 441648229, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 365036545, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 441648229}},
        {'text_pos': 720, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 365036545, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 352584678, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 441648229, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 352584678}},
        {'text_pos': 751, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 441648229, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 477889682, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 352584678, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 477889682}},
        {'text_pos': 779, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 352584678, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 140640874, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 477889682, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 140640874}},
        {'text_pos': 807, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 477889682, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 534447323, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 140640874, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 534447323}},
        {'text_pos': 829, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 140640874, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 442500214, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 534447323, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 442500214}},
        {'text_pos': 857, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 534447323, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 526189735, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 442500214, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 526189735}},
        {'text_pos': 884, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 442500214, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 531104992, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 526189735, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 531104992}},
        {'text_pos': 922, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 526189735, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 448595053, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 531104992, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 448595053}},
        {'text_pos': 950, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 531104992, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 525534421, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 448595053, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 525534421}},
        {'text_pos': 978, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 448595053, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 1033438964, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 525534421, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 1033438964}},
        {'text_pos': 1000, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 525534421, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 590284051, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 1033438964, 'r_-13': 4, 'r_-18': 5, 'r_-4': 5, 'r_-8': 4, 'r_-14': 3, 'l_-3': 590284051}},
        {'text_pos': 1034, 'atts': {'c_-1': 0, 'r_-2': 5636168, 'r_-19': 21102779, 'r_-5': 21102779, 'r_-7': 3, 'r_-17': 1033438964, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 5, 'r_-15': 4, 'r_-1': 4, 'r_-20': 4, 'r_-3': 784270826, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 590284051, 'r_-13': 4, 'r_-18': 5, 'l_-3': 784270826, 'r_-8': 4, 'r_-14': 3, 'r_-4': 5}},
        {'text_pos': 1059, 'atts': {'c_-1': 0, 'r_-2': 5636168, 'r_-19': 3, 'r_-5': 3, 'r_-7': 5636168, 'r_-17': 21102779, 'l_-1': 4, 'r_-9': 5, 'r_-11': 4, 'l_1': 5, 'r_-15': 590284051, 'r_-1': 4, 'r_-20': 4, 'r_-3': 680265064, 'r_-12': 3, 'r_-16': 5, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 21102779, 'r_-13': 4, 'r_-18': 4, 'l_-3': 680265064, 'r_-8': 784270826, 'r_-14': 5636168, 'r_-4': 5}},
        {'text_pos': 1084, 'atts': {'c_-1': 0, 'r_-2': 5636168, 'r_-19': 5636168, 'r_-5': 3, 'r_-7': 5636168, 'r_-17': 3, 'l_-1': 4, 'r_-9': 5, 'r_-11': 4, 'l_1': 5, 'r_-15': 21102779, 'r_-1': 4, 'r_-20': 590284051, 'r_-3': 685770117, 'r_-12': 5636168, 'r_-16': 4, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 784270826, 'r_-18': 4, 'l_-3': 685770117, 'r_-8': 680265064, 'r_-14': 5, 'r_-4': 5}},
        {'text_pos': 1109, 'atts': {'c_-1': 0, 'r_-2': 5636168, 'r_-19': 5, 'r_-5': 3, 'r_-7': 5636168, 'r_-17': 5636168, 'l_-1': 4, 'r_-9': 5, 'r_-11': 4, 'l_1': 5, 'r_-15': 3, 'r_-1': 4, 'r_-20': 21102779, 'r_-3': 686687632, 'r_-12': 5636168, 'r_-16': 4, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 680265064, 'r_-18': 784270826, 'l_-3': 686687632, 'r_-8': 685770117, 'r_20': 2, 'r_-14': 5, 'r_-4': 5}},
        {'text_pos': 1131, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 5, 'r_-5': 3, 'r_-7': 5636168, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 5636168, 'l_-1': 4, 'r_-9': 5, 'r_-11': 4, 'l_1': 4, 'r_-15': 3, 'r_-1': 4, 'r_-20': 3, 'r_-3': 530187503, 'r_-12': 5636168, 'r_-16': 4, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 3, 'r_-13': 685770117, 'r_15': 2, 'r_-18': 680265064, 'r_-4': 5, 'r_-8': 686687632, 'r_-14': 5, 'l_-3': 530187503}},
        {'text_pos': 1158, 'atts': {'l_3': 5, 'l_2': 21102779, 'r_-19': 5636168, 'r_-5': 21102779, 'r_-7': 3, 'c_-1': 0, 'r_-2': 5636168, 'r_-17': 3, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'l_1': 4, 'r_-15': 686687632, 'r_-1': 4, 'r_-20': 685770117, 'r_-3': 426574886, 'r_-12': 3, 'r_-16': 5, 'c_1': 0, 'r_-6': 4, 'r_8': 2, 'l_-2': 5636168, 'r_-10': 530187503, 'r_-13': 4, 'r_-18': 4, 'r_-4': 5, 'r_-8': 4, 'r_-14': 5636168, 'l_-3': 426574886}},
        {'text_pos': 1184, 'atts': {'c_-1': 0, 'r_-2': 5636168, 'r_-19': 3, 'r_-5': 21102779, 'l_0': 5, 'r_-17': 530187503, 'l_-1': 4, 'r_-9': 5636168, 'r_-11': 5, 'r_-1': 4, 'r_-15': 4, 'r_-20': 4, 'r_-3': 424346630, 'r_-12': 21102779, 'r_-16': 5636168, 'c_1': 0, 'r_-6': 4, 'l_-2': 5636168, 'r_-10': 426574886, 'r_-13': 4, 'r_-18': 5, 'r_1': 2, 'l_-3': 424346630, 'r_-8': 4, 'r_-7': 3, 'r_-14': 3, 'r_-4': 5}}
        ]
        text='MemTotal:        3085780 kB\nMemFree:          835216 kB\nMemAvailable:    1509660 kB\nBuffers:          304576 kB\nCached:           304132 kB\nSwapCached:            0 kB\nActive:           734184 kB\nInactive:         155608 kB\nActive(anon):     304772 kB\nInactive(anon):      344 kB\nActive(file):     429412 kB\nInactive(file):   155264 kB\nUnevictable:     1192276 kB\nMlocked:         1192276 kB\nSwapTotal:             0 kB\nSwapFree:              0 kB\nDirty:               344 kB\nWriteback:             0 kB\nAnonPages:       1382500 kB\nMapped:            58880 kB\nShmem:              1184 kB\nSlab:             142336 kB\nSReclaimable:     129504 kB\nSUnreclaim:        12832 kB\nKernelStack:        2784 kB\nPageTables:         7672 kB\nNFS_Unstable:          0 kB\nBounce:                0 kB\nWritebackTmp:          0 kB\nCommitLimit:     1542888 kB\nCommitted_AS:    1548912 kB\nVmallocTotal:   34359738367 kB\nVmallocUsed:           0 kB\nVmallocChunk:          0 kB\nHardwareCorrupted:     0 kB\nAnonHugePages:   1255424 kB\nHugePages_Total:       0\nHugePages_Free:        0\nHugePages_Rsvd:        0\nHugePages_Surp:        0\nHugepagesize:       2048 kB\nDirectMap4k:       44992 kB\nDirectMap2M:     3100672 kB\n'
        hashed_text=varapi.get_hashed_text(text)
        var_atts2=varapi.get_variables_atts(hashed_text)
        self.assertEqual(var_atts, var_atts2)

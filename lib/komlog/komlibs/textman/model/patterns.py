'''

this file defines some patterns for regular expressions

'''

import re

# patterns used for variable identification


VAR_PREFIX_SEPARATOR_REGEXP = '(?<=[ \s/\|\(\[\];:\*%$#"=\'\{\}])'
VAR_SUFIX_SEPARATOR_REGEXP  = '(?=([ \s/\|\)\[\];:\*%$#"=\'\{\}]|, ))' #we add ', ' for the top command case to detect load_averages, for example.
VAR_PREFIX_SEPARATOR_WITH_COMMA_REGEXP = '(?<=[, \s/\|\(\[\];:\*%$#"=\'\{\}])'
VAR_SUFIX_SEPARATOR_WITH_COMMA_REGEXP = '(?=[, \s/\|\(\[\];:\*%$#"=\'\{\}])'

SEPARATOR_REGEXP = '([ ]+|[\s/\|\(\)\[\];:\*\.%\$\#"=])'
WORD_REGEXP = '([A-Za-z0-9_]+)'
NUMBER_REGEXP = '([0-9]+)'
SPACES_REGEXP = '([ ]+)'
NEWLINE_REGEXP = '(\n)'
ANYTHING_REGEXP = '(.{1})'
JSON_NEWLINE = '(}, {)'
JSON_SEPARATOR = '(: |, )'

FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA = '([-+]?[0-9]{1,3}(\.[0-9][0-9][0-9])+[,][0-9]+)'
FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT = '([-+]?[0-9]{1,3}(,[0-9][0-9][0-9])+[\.][0-9]+)'
FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA = '([-+]?[0-9]{4,}[,][0-9]+)'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA = '([-+]?[0-9]{0,3}[,][0-9]{4,})'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA = '([-+]?[0-9]{0,3}[,][0-9]{1,2})'
FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA = '([-+]?[,][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA = '([-+]?[0][,][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT = '([-+]?[0-9]{4,}[\.][0-9]+)'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT = '([-+]?[0-9]{0,3}[\.][0-9]{4,})'
FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT = '([-+]?[0-9]{0,3}[\.][0-9]{1,2})'
FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT = '([-+]?[\.][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT = '([-+]?[0][\.][0-9]{3})'
FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP = '([-+]?[0-9]{1,3}[\.,][0-9]{3})'
INTEGER_LEFT_TO_RIGHT = '([-+]?[0-9]+)'
FLOAT_LEFT_TO_RIGHT_CSV_FORMATTED = '('+VAR_PREFIX_SEPARATOR_WITH_COMMA_REGEXP+'[-+]?[0-9]*[\.]?[0-9]+'+VAR_SUFIX_SEPARATOR_WITH_COMMA_REGEXP+'|^[-+]?[0-9]*[\.]?[0-9]+'+VAR_SUFIX_SEPARATOR_WITH_COMMA_REGEXP+'|'+VAR_PREFIX_SEPARATOR_WITH_COMMA_REGEXP+'[-+]?[0-9]*[\.]?[0-9]+$)'

#we have create regex like this because variable-width look-aheads and look-behinds are not supported

ro_var_regex_0 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_COMMA+'$')

ro_var_regex_1 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_WITH_THOUSAND_SEPARATOR_AND_DECSEP_DOT+'$')

ro_var_regex_2 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_COMMA+'$')

ro_var_regex_3 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_COMMA+'$')

ro_var_regex_4 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_COMMA+'$')

ro_var_regex_5 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_COMMA+'$')

ro_var_regex_6 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_COMMA+'$')

ro_var_regex_7 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_4_ORDER_OR_MORE_AND_DECIMAL_ANY_ORDER_DECSEP_DOT+'$')

ro_var_regex_8 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_4_ORDER_OR_MORE_DECSEP_DOT+'$')

ro_var_regex_9 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_3_ORDER_AND_DECIMAL_1_2_ORDER_DECSEP_DOT+'$')

ro_var_regex_10 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_ORDER_AND_DECIMAL_3_ORDER_DECSEP_DOT+'$')

ro_var_regex_11 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_0_VALUE_AND_DECIMAL_3_ORDER_DECSEP_DOT+'$')

ro_var_regex_12 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+FLOAT_LEFT_TO_RIGHT_INT_1_3_ORDER_AND_DECIMAL_3_ORDER_AMBIGUOS_DECSEP+'$') #the can match values like 0,232 o 0.432, check the 0_VALUE regex before this, so we dont have to complicate the expression of this one

ro_var_regex_13 = re.compile(VAR_PREFIX_SEPARATOR_REGEXP+INTEGER_LEFT_TO_RIGHT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          '^'+INTEGER_LEFT_TO_RIGHT+VAR_SUFIX_SEPARATOR_REGEXP+'|'+\
                          VAR_PREFIX_SEPARATOR_REGEXP+INTEGER_LEFT_TO_RIGHT+'$')

ro_var_regex_14 = re.compile(FLOAT_LEFT_TO_RIGHT_CSV_FORMATTED)

ro_hash = re.compile(JSON_NEWLINE+'|'+JSON_SEPARATOR+'|'+SEPARATOR_REGEXP+'|'+WORD_REGEXP+'|'+NUMBER_REGEXP+'|'+ANYTHING_REGEXP)
ro_number = re.compile(NUMBER_REGEXP)
ro_spaces = re.compile(JSON_SEPARATOR+'|'+SPACES_REGEXP)
ro_newline = re.compile(JSON_NEWLINE+'|'+NEWLINE_REGEXP)

VAR_REGEXP_OBJECTS = [ro_var_regex_0,
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


# patterns used for text tokenization

TEXT_TOKENIZATION_SYMBOL_REGEXP = '[ \n\t/\|\(\)\[\];:\.%\$\#"=]'
TEXT_TOKENIZATION_WORD_REGEXP = '([0-9]*[A-Za-z_/]+[0-9]*)+'

ro_text_tokenization = re.compile('('+TEXT_TOKENIZATION_WORD_REGEXP+'|'+TEXT_TOKENIZATION_SYMBOL_REGEXP+')')

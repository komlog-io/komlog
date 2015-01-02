#coding:utf-8

import unittest
import uuid
import datetime
from komlibs.general.validation import arguments

class GeneralValidationArgumentsTest(unittest.TestCase):
    ''' komlog.general.validation.arguments tests '''

    def test_is_valid_username_invalid(self):
        ''' is_valid_username should fail if username is not valid '''
        params=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter']
        for param in params:
            self.assertFalse(arguments.is_valid_username(param)) 

    def test_is_valid_username_valid(self):
        ''' is_valid_username should succeed if username is valid '''
        usernames=['test_user']
        for username in usernames:
            self.assertTrue(arguments.is_valid_username(username)) 

    def test_is_valid_agentname_invalid(self):
        ''' is_valid_agentname should fail if agentname is not valid '''
        params=[None, 234234, 'Agentname with \t is not Valid','Agentname with \n neither']
        for param in params:
            self.assertFalse(arguments.is_valid_agentname(param)) 

    def test_is_valid_agentname_valid(self):
        ''' is_valid_agentname should succeed if agentname is valid '''
        params=['test_agent', 'Agentname OK', 'Agentname @213 #23']
        for param in params:
            self.assertTrue(arguments.is_valid_agentname(param)) 

    def test_is_valid_datasourcename_invalid(self):
        ''' is_valid_datasourcename should fail if datasourcename is not valid '''
        params=[None, 234234, 'Datasource with \n is not valid', 'Datasource with \t not valid']
        for param in params:
            self.assertFalse(arguments.is_valid_datasourcename(param)) 

    def test_is_valid_datasourcename_valid(self):
        ''' is_valid_datasourcename should succeed if datasourcename is valid '''
        params=['Datasource Name','DatasourceName','234234','#1 Datasource','Datasource 234234','Con caracteres #@$%&+=_.- por ejemplo']
        for param in params:
            self.assertTrue(arguments.is_valid_datasourcename(param)) 

    def test_is_valid_datapointname_invalid(self):
        ''' is_valid_datapointname should fail if datapointname is not valid '''
        params=[None, 234234, 'Datapoints with \n are not valid', 'Datapoint with \t not valid']
        for param in params:
            self.assertFalse(arguments.is_valid_datapointname(param)) 

    def test_is_valid_datapointname_valid(self):
        ''' is_valid_datapointname should succeed if datapointname is valid '''
        params=['Datapoint Name','DatapointName','234234','#1 Datapoint','Datapoint 234234','Con caracteres #@$%&+=_.- por ejemplo']
        for param in params:
            self.assertTrue(arguments.is_valid_datapointname(param)) 

    def test_is_valid_datasource_content_invalid(self):
        ''' is_valid_datasource_content should fail if datasource_content is not valid '''
        params=[None, 234234]
        for param in params:
            self.assertFalse(arguments.is_valid_datasource_content(param)) 

    def test_is_valid_datasource_content_valid(self):
        ''' is_valid_datasource_content should succeed if datasource_content is valid '''
        params=['test_agent']
        for param in params:
            self.assertTrue(arguments.is_valid_datasource_content(param)) 

    def test_is_valid_password_invalid(self):
        ''' is_valid_password should fail if password is not valid '''
        params=[None, 234234, 'with spaces is not valid by now','onlyasciiÑ']
        for param in params:
            self.assertFalse(arguments.is_valid_password(param)) 

    def test_is_valid_password_valid(self):
        ''' is_valid_password should succeed if password is valid '''
        params=['123123A#','12!password','ApasswordWithNumbers43343AndCAPITALSandsimbols+']
        for param in params:
            self.assertTrue(arguments.is_valid_password(param)) 

    def test_is_valid_email_invalid(self):
        ''' is_valid_email should fail if email is not valid '''
        params=[None, 234234,'not_an_email','email.com','@domain.com','email@','email@domain@domain.com','español@domain.com']
        for param in params:
            self.assertFalse(arguments.is_valid_email(param)) 

    def test_is_valid_email_valid(self):
        ''' is_valid_email should succeed if email is valid '''
        params=['my_email@domain.com','my.email@mydomain.es','thisEmailIsValid@yahoo.com','info@subdomain.domain.com']
        for param in params:
            self.assertTrue(arguments.is_valid_email(param)) 

    def test_is_valid_code_invalid(self):
        ''' is_valid_code should fail if code is not valid '''
        params=[None, 234234,'spaces not allowed','Only ASCII ÑÑ','notallowed\'#$%&/()@"!','\n','\t']
        for param in params:
            self.assertFalse(arguments.is_valid_code(param)) 

    def test_is_valid_code_valid(self):
        ''' is_valid_code should succeed if code is valid '''
        params=['testcode']
        for param in params:
            self.assertTrue(arguments.is_valid_code(param)) 

    def test_is_valid_pubkey_invalid(self):
        ''' is_valid_pubkey should fail if pubkey is not valid '''
        params=[None, 234234,'Only ASCII ÑÑ','tabulators not allowed \t','semicolon not allowed ;']
        for param in params:
            self.assertFalse(arguments.is_valid_pubkey(param)) 

    def test_is_valid_pubkey_valid(self):
        ''' is_valid_pubkey should succeed if pubkey is valid '''
        params=['pubkey','Spaces allowed','New lines \n allowed','other chars allowed +/-']
        for param in params:
            self.assertTrue(arguments.is_valid_pubkey(param)) 

    def test_is_valid_version_invalid(self):
        ''' is_valid_version should fail if version is not valid '''
        params=[None, 234234]
        for param in params:
            self.assertFalse(arguments.is_valid_version(param)) 

    def test_is_valid_version_valid(self):
        ''' is_valid_version should succeed if version is valid '''
        params=['version','version: 1.2','v2.0.0 codenamed: X']
        for param in params:
            self.assertTrue(arguments.is_valid_version(param)) 

    def test_is_valid_uuid_invalid(self):
        ''' is_valid_uuid should fail if uuid is not valid '''
        params=[None, 234234,'string','string with spaces','234234']
        for param in params:
            self.assertFalse(arguments.is_valid_uuid(param)) 

    def test_is_valid_uuid_valid(self):
        ''' is_valid_uuid should succeed if version is valid '''
        params=[uuid.uuid4()]
        for param in params:
            self.assertTrue(arguments.is_valid_uuid(param)) 

    def test_is_valid_dict_invalid(self):
        ''' is_valid_dict should fail if dict is not valid '''
        params=[None, 234234,'string','string with spaces','234234']
        for param in params:
            self.assertFalse(arguments.is_valid_dict(param)) 

    def test_is_valid_dict_valid(self):
        ''' is_valid_dict should succeed if dict is valid '''
        params=[{}, {'prueba':'value'}]
        for param in params:
            self.assertTrue(arguments.is_valid_dict(param)) 

    def test_is_valid_bool_invalid(self):
        ''' is_valid_bool should fail if bool is not valid '''
        params=[None, 234234,'string','string with spaces','234234']
        for param in params:
            self.assertFalse(arguments.is_valid_bool(param)) 

    def test_is_valid_bool_valid(self):
        ''' is_valid_bool should succeed if bool is valid '''
        params=[True,False]
        for param in params:
            self.assertTrue(arguments.is_valid_bool(param)) 

    def test_is_valid_string_int_invalid(self):
        ''' is_valid_string_int should fail if input is not valid '''
        params=[None, 234234,'string','string with spaces','#234234','234231000$','23422343€','234234.234234']
        for param in params:
            self.assertFalse(arguments.is_valid_string_int(param)) 

    def test_is_valid_string_int_valid(self):
        ''' is_valid_string_int should succeed if input is valid '''
        params=['1','000001','123123123123','0']
        for param in params:
            self.assertTrue(arguments.is_valid_string_int(param)) 

    def test_is_valid_date_invalid(self):
        ''' is_valid_date should fail if input is not valid date'''
        params=[None, 234234,'string','string with spaces','#234234','2014-12-10']
        for param in params:
            self.assertFalse(arguments.is_valid_date(param)) 

    def test_is_valid_date_valid(self):
        ''' is_valid_date should succeed if input is valid date'''
        params=[datetime.datetime.utcnow()]
        for param in params:
            self.assertTrue(arguments.is_valid_date(param)) 

    def test_is_valid_hexcolor_invalid(self):
        ''' is_valid_hexcolor should fail if input is not valid hex color (with #)'''
        params=[None, 234234,'string','string with spaces','23#4234','2014-12-10','332255','#FFGGFF','#0012HD','#ÑÑÑÑÑÑ','#0123vd']
        for param in params:
            self.assertFalse(arguments.is_valid_hexcolor(param)) 

    def test_is_valid_hexcolor_valid(self):
        ''' is_valid_hexcolor should succeed if input is valid hex color (with #)'''
        params=['#BBCCDD','#aa0033','#AA0033','#FFFFFF','#FFffff','#000000','#FF0000','#00FF00','#0000FF','#FF00FF','#FFFF00','#00FFFF','#AABBCC','#001234','#99807F','#4A5F6E']
        for param in params:
            self.assertTrue(arguments.is_valid_hexcolor(param)) 


import unittest
from komlog.komfs import api

class KomfsApiTest(unittest.TestCase):
    ''' komlog.komfs.api tests '''

    def test_create_sample_success(self):
        ''' create_sample should succeed if filename can be created and content is valid '''
        filename='/tmp/test_create_sample_success.txt'
        data='TEST CONTENT'
        self.assertTrue(api.create_sample(filename=filename, data=data))

    def test_create_sample_failure_invalid_filename(self):
        ''' create_sample should fail if filename is wrong '''
        files=[3234234234234,None,{},[3242342,],(2342,234234)]
        data='TEST CONTENT'
        for filename in files:
            self.assertFalse(api.create_sample(filename=filename, data=data))

    def test_create_sample_failure_no_permission(self):
        ''' create_sample should fail if filename cannot be created '''
        filename='/root/test_create_sample_failure_no_permission.txt'
        data='TEST CONTENT'
        self.assertFalse(api.create_sample(filename=filename, data=data))

    def test_create_sample_failure_invalid_content(self):
        ''' create_sample should fail if content is not valid '''
        filename='/tmp/test_create_sample_failure_invalid_content.txt'
        datas=[3234234234234,None,{},[3242342,],(2342,234234)]
        for data in datas:
            self.assertFalse(api.create_sample(filename=filename, data=data))

    def test_get_file_content_success(self):
        ''' get_file_content should succeed if file exists and can be read '''
        filename='/tmp/test_get_file_content_success.txt'
        data='CONTENT \nTEST\t WITH\t SOME\t UTF-8 CHARS ÑÑÑÑ'
        api.create_sample(filename=filename, data=data)
        self.assertEqual(api.get_file_content(filename=filename),data)

    def test_get_file_content_failure_invalid_filename(self):
        ''' get_file_content should succeed if file exists and can be read '''
        files=[3234234234234,None,{},[3242342,],(2342,234234)]
        for filename in files:
            self.assertIsNone(api.get_file_content(filename=filename))

    def test_get_file_content_failure_non_existent_filename(self):
        ''' get_file_content should succeed if file exists and can be read '''
        filename='/tmp/test_get_file_content_failure_non_existent_filename.txt'
        self.assertIsNone(api.get_file_content(filename=filename))


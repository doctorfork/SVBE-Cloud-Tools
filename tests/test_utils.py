import utils
import unittest

class ConvertMapToCamelCaseTest(unittest.TestCase):
    
    def testConvertMultiLevel(self):
        d = {'test_key': {'test_key_two': 'foo'}}
        expected = {'testKey': {'testKeyTwo': 'foo'}}
        
        actual = utils.ConvertDictKeysToCamelCase(d)
        
        self.assertDictEqual(actual, expected)
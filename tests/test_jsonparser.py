import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from MagisterPy import JsParser

import unittest
import json
  # Replace with the actual module name where JsParser is defined

class TestJsParser(unittest.TestCase):
    def setUp(self):
        """Set up a JsParser instance for testing."""
        self.parser = JsParser()

    def test_valid_authcode_extraction(self):
        with open(r"tests\test_javascripts\account-85bb24d85718eb247b7c.js") as file:
            content = file.read()
            self.assertEqual(self.parser.get_authcode_from_js(content),"1ca5d248")


        with open(r"tests\test_javascripts\account-e6fb87fd4f567cbd37f5.js") as file:
            content = file.read()
            self.assertEqual(self.parser.get_authcode_from_js(content),"b7cf076f")
        

if __name__ == "__main__":
    unittest.main()

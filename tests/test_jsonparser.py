import json
import unittest
from MagisterPy import JsParser
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))


# Replace with the actual module name where JsParser is defined


class TestJsParser(unittest.TestCase):
    def setUp(self):
        """Set up a JsParser instance for testing."""
        self.parser = JsParser()

    def test_valid_authcode_extraction(self):
        with open(r"tests\test_javascripts\account-56c22c13622e321fb1f1.js") as file:
            content = file.read()
            self.assertEqual(self.parser.get_authcode_from_js(
                content), "6380e45e80d5bb")


if __name__ == "__main__":
    unittest.main()

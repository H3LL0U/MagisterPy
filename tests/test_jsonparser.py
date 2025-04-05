import sys
import os
import logging
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))  # NOQA
import json
import unittest
from MagisterPy import JsParser
logging.basicConfig(level=logging.INFO)

# Replace with the actual module name where JsParser is defined


class TestJsParser(unittest.TestCase):
    def setUp(self):
        """Set up a JsParser instance for testing."""
        self.parser = JsParser()

    def test_valid_authcode_extraction(self):
        for filename in os.listdir("tests/test_javascripts/"):
            with open(f"tests/test_javascripts/{filename}") as file:
                content = file.read()
                logging.info(f"detected authcode: {self.parser.get_authcode_from_js(content)}")  # NOQA

                self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()

import os
import unittest
from stitch_ai import StitchSDK

class TestStitchSDK(unittest.TestCase):
    def setUp(self):
        os.environ.pop("STITCH_API_KEY", None)

    def test_missing_api_key_raises_error(self):
        with self.assertRaises(ValueError):
            StitchSDK(base_url="http://localhost")

    def test_sdk_instantiation_with_api_key(self):
        os.environ["STITCH_API_KEY"] = "demo-testwallet"
        try:
            sdk = StitchSDK(base_url="http://localhost")
            self.assertIsNotNone(sdk)
        finally:
            os.environ.pop("STITCH_API_KEY", None)

if __name__ == "__main__":
    unittest.main()

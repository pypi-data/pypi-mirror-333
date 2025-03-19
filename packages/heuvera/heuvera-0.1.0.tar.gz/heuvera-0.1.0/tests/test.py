import unittest
from heuvera.client import Heuvera
from heuvera.otp import OTP
from heuvera.types import GenerateOTPRequest, VerifyOTPRequest


class TestOTP(unittest.TestCase):
    def setUp(self):
        self.client = Heuvera("api-key")
        self.otp = OTP(self.client)

    def test_generate_otp(self):
        request = GenerateOTPRequest(length=6, expiresIn=10)
        response = self.otp.generate(request)
        self.assertIn("otp", response)

    def test_verify_otp(self):
        request = VerifyOTPRequest(code="123456")
        response = self.otp.verify(request)
        self.assertIn("valid", response)


if __name__ == "__main__":
    unittest.main()

import unittest
from ai_img_gen.exceptions import (
    AIImageGeneratorError,
    APIError,
    ValidationError,
    AuthenticationError,
    RateLimitError
)


class TestExceptions(unittest.TestCase):
    def test_ai_image_generator_error(self):
        error = AIImageGeneratorError("Test error")
        self.assertEqual(str(error), "Test error")

    def test_api_error(self):
        error = APIError(500, "Internal server error")
        self.assertEqual(error.status_code, 500)
        self.assertEqual(error.message, "Internal server error")
        self.assertEqual(str(error), "API Error (500): Internal server error")

    def test_validation_error(self):
        error = ValidationError("Invalid input")
        self.assertEqual(str(error), "Invalid input")

    def test_authentication_error(self):
        error = AuthenticationError("Invalid API key")
        self.assertEqual(str(error), "Invalid API key")

    def test_rate_limit_error(self):
        # Test with default message
        error = RateLimitError()
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.message, "Rate limit exceeded")
        self.assertEqual(str(error), "API Error (429): Rate limit exceeded")

        # Test with custom message
        error = RateLimitError("Too many requests")
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.message, "Too many requests")
        self.assertEqual(str(error), "API Error (429): Too many requests")


if __name__ == '__main__':
    unittest.main()
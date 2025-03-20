import unittest
from unittest.mock import patch, MagicMock
from ai_img_gen import (
    AIImageGeneratorClient,
    ClientConfig,
    ImageGenerationOptions,
    ResizeImageOptions,
    ConvertImageOptions,
    OptimizeImageOptions,
    APIError,
    ValidationError,
    AuthenticationError
)


class TestAIImageGeneratorClient(unittest.TestCase):
    def setUp(self):
        self.client = AIImageGeneratorClient(
            ClientConfig(
                base_url="https://api.img-gen.ai",
                api_key="test_api_key"
            )
        )

    @patch('ai_img_gen.client.requests.request')
    def test_generate_image(self, mock_request):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.url = "https://api.img-gen.ai/images/test.png"
        mock_request.return_value = mock_response

        # Test generate_image method
        options = ImageGenerationOptions(
            width=512,
            height=512,
            prompt="E-Commerce Platform Web Development",
            model="dall-e-2",
            format="png",
            quality=90,
            optimize=True
        )

        result = self.client.generate_image(options)
        self.assertEqual(result, "https://ai-img-gen-test.s3.us-east-1.amazonaws.com/images/1741921240638_512x512_dall-e-2_d7a5dc07_026c444e.png")

        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['method'], 'GET')
        self.assertEqual(kwargs['url'], 'https://api.img-gen.ai/images/image-gen')
        self.assertEqual(kwargs['params']['width'], 512)
        self.assertEqual(kwargs['params']['height'], 512)
        self.assertEqual(kwargs['params']['prompt'], "Test prompt")
        self.assertEqual(kwargs['params']['model'], "dall-e-2")
        self.assertEqual(kwargs['params']['format'], "png")
        self.assertEqual(kwargs['params']['quality'], 90)
        self.assertEqual(kwargs['params']['optimize'], "true")

    @patch('ai_img_gen.client.requests.request')
    def test_get_supported_models(self, mock_request):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["dall-e-2", "openai"]
        mock_request.return_value = mock_response

        # Test get_supported_models method
        result = self.client.get_supported_models()
        self.assertEqual(result, ["dall-e-2", "openai"])

        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['method'], 'GET')
        self.assertEqual(kwargs['url'], 'https://api.img-gen.ai/images/supported-models')

    @patch('ai_img_gen.client.requests.request')
    def test_resize_image(self, mock_request):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.url = "https://api.img-gen.ai/images/resized.png"
        mock_request.return_value = mock_response

        # Test resize_image method
        options = ResizeImageOptions(
            width=256,
            height=256,
            format="png",
            quality=90
        )

        result = self.client.resize_image("a7ee365a-c024-4d2d-91db-598f2be8ef45", options)
        self.assertEqual(result, "https://ai-img-gen-test.s3.us-east-1.amazonaws.com/images/1741921240638_512x512_dall-e-2_d7a5dc07_026c444e.png")

        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['method'], 'GET')
        self.assertEqual(kwargs['url'], 'https://api.img-gen.ai/images/process/resize/test_image_id')
        self.assertEqual(kwargs['params']['width'], 256)
        self.assertEqual(kwargs['params']['height'], 256)
        self.assertEqual(kwargs['params']['format'], "png")
        self.assertEqual(kwargs['params']['quality'], 90)

    @patch('ai_img_gen.client.requests.request')
    def test_api_error(self, mock_request):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_request.return_value = mock_response

        # Test error handling
        options = ImageGenerationOptions(
            width=512,
            height=512,
            prompt="Test prompt"
        )

        with self.assertRaises(APIError) as context:
            self.client.generate_image(options)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "Internal server error")

    @patch('ai_img_gen.client.requests.request')
    def test_authentication_error(self, mock_request):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_request.return_value = mock_response

        # Test authentication error
        options = ImageGenerationOptions(
            width=512,
            height=512,
            prompt="Test prompt"
        )

        with self.assertRaises(AuthenticationError):
            self.client.generate_image(options)


if __name__ == '__main__':
    unittest.main()
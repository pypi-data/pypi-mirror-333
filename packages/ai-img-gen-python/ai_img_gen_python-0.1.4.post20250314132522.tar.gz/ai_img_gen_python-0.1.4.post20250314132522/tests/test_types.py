import unittest
from ai_img_gen.types import (
    ClientConfig,
    ImageGenerationOptions,
    ResizeImageOptions,
    ConvertImageOptions,
    OptimizeImageOptions,
    HealthStatus,
    Metrics
)


class TestTypes(unittest.TestCase):
    def test_client_config(self):
        # Test with required parameters only
        config = ClientConfig(base_url="https://api.img-gen.ai")
        self.assertEqual(config.base_url, "https://api.img-gen.ai")
        self.assertIsNone(config.api_key)
        self.assertEqual(config.timeout, 30)

        # Test with all parameters
        config = ClientConfig(
            base_url="https://api.img-gen.ai",
            api_key="test_api_key",
            timeout=60
        )
        self.assertEqual(config.base_url, "https://api.img-gen.ai")
        self.assertEqual(config.api_key, "test_api_key")
        self.assertEqual(config.timeout, 60)

    def test_image_generation_options(self):
        # Test with required parameters only
        options = ImageGenerationOptions(
            width=512,
            height=512,
            prompt="Test prompt"
        )
        self.assertEqual(options.width, 512)
        self.assertEqual(options.height, 512)
        self.assertEqual(options.prompt, "Test prompt")
        self.assertEqual(options.model, "dall-e-2")
        self.assertEqual(options.format, "png")
        self.assertEqual(options.quality, 90)
        self.assertTrue(options.optimize)

        # Test with all parameters
        options = ImageGenerationOptions(
            width=1024,
            height=768,
            prompt="Custom prompt",
            model="custom-model",
            format="jpeg",
            quality=75,
            optimize=False
        )
        self.assertEqual(options.width, 1024)
        self.assertEqual(options.height, 768)
        self.assertEqual(options.prompt, "Custom prompt")
        self.assertEqual(options.model, "custom-model")
        self.assertEqual(options.format, "jpeg")
        self.assertEqual(options.quality, 75)
        self.assertFalse(options.optimize)

    def test_resize_image_options(self):
        options = ResizeImageOptions(
            width=256,
            height=256,
            format="png",
            quality=90
        )
        self.assertEqual(options.width, 256)
        self.assertEqual(options.height, 256)
        self.assertEqual(options.format, "png")
        self.assertEqual(options.quality, 90)

    def test_convert_image_options(self):
        options = ConvertImageOptions(
            format="jpeg",
            quality=85
        )
        self.assertEqual(options.format, "jpeg")
        self.assertEqual(options.quality, 85)

    def test_optimize_image_options(self):
        options = OptimizeImageOptions(
            format="webp",
            quality=75
        )
        self.assertEqual(options.format, "webp")
        self.assertEqual(options.quality, 75)

    def test_health_status(self):
        status = HealthStatus(
            status="ok",
            info={"version": "1.0.0"},
            error=None,
            details={"uptime": 3600}
        )
        self.assertEqual(status.status, "ok")
        self.assertEqual(status.info, {"version": "1.0.0"})
        self.assertIsNone(status.error)
        self.assertEqual(status.details, {"uptime": 3600})

    def test_metrics(self):
        metrics = Metrics(
            requests=100,
            images_generated=50,
            average_response_time=250.5
        )
        self.assertEqual(metrics.requests, 100)
        self.assertEqual(metrics.images_generated, 50)
        self.assertEqual(metrics.average_response_time, 250.5)


if __name__ == '__main__':
    unittest.main()
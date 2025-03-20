# AI Image Generator Python SDK

[![PyPI version](https://img.shields.io/pypi/v/ai-img-gen-python.svg)](https://pypi.org/project/ai-img-gen-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/ai-img-gen-python.svg)](https://pypi.org/project/ai-img-gen-python/)

A Python SDK for interacting with the AI Image Generator API.

## Installation

```bash
pip install ai-img-gen-python
```


### Quick Start
```python
from ai_img_gen import AIImageGeneratorClient, ClientConfig, ImageGenerationOptions

# Initialize the client
client = AIImageGeneratorClient(
    ClientConfig(
        base_url="https://api.img-gen.ai",
        api_key="your_api_key_here"
    )
)
```

# Generate an image
```python
options = ImageGenerationOptions(
    width=512,
    height=512,
    prompt="A futuristic city with flying cars and neon lights",
    model="dall-e-2",
    format="png",
    quality=90,
    optimize=True
)

image_url = client.generate_image(options)
print(f"Generated image URL: {image_url}")
```

7. Let's create a basic example:

```python
from ai_img_gen import AIImageGeneratorClient, ClientConfig, ImageGenerationOptions

# Initialize the client
client = AIImageGeneratorClient(
    ClientConfig(
        base_url="https://api.img-gen.ai",
        api_key="your_api_key_here"
    )
)

# Generate an image
options = ImageGenerationOptions(
    width=512,
    height=512,
    prompt="A futuristic city with flying cars and neon lights",
    model="dall-e-2",
    format="png",
    quality=90,
    optimize=True
)

image_url = client.generate_image(options)
print(f"Generated image URL: {image_url}")
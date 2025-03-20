from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-img-gen-python",
    version="0.1.0",
    author="skbhati199",
    author_email="skbhati199@gmail.com",
    description="Python SDK for AI Image Generator API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skbhati199/ai-img-gen-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
)
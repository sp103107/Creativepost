from setuptools import setup, find_packages

# Read README.md if it exists, otherwise use a default description
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A comprehensive content generation and processing pipeline."

setup(
    name="content-pipeline",
    version="0.1.0",
    packages=find_packages(include=['content_pipeline', 'content_pipeline.*']),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "Pillow>=9.5.0",
        "numpy>=1.24.0",
        "diffusers>=0.17.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.8.0",
        "pytest>=7.3.0",
        "pytest-asyncio>=0.21.0",
        "moviepy>=1.0.3",
        "soundfile>=0.12.1"
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-asyncio',
            'black',
            'isort',
            'mypy',
            'flake8'
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive content generation and processing pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/content-pipeline",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

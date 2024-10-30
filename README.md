# Content Pipeline

A comprehensive content generation and processing pipeline.

## Installation

```bash
pip install -e .
```

## Usage

```python
from content_pipeline.generation import ContentCreator

creator = ContentCreator()
content = await creator.create_content(
    content_type="blog_post",
    prompt="Write about AI"
)
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest tests/
   ```

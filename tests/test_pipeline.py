import pytest
from content_pipeline.generation import ContentGenerator

def test_simple():
    """A simple test to verify pytest is working"""
    assert True

def test_imports():
    """Test that we can import our modules"""
    generator = ContentGenerator("dummy_api_key")
    assert isinstance(generator, ContentGenerator)

@pytest.mark.asyncio
async def test_content_generation():
    """Test basic content generation"""
    generator = ContentGenerator("dummy_api_key")
    content = await generator.generate_content(
        topic="AI",
        style="professional",
        tone="friendly"
    )
    assert content is not None
    assert isinstance(content, dict)

if __name__ == '__main__':
    pytest.main(['-v'])

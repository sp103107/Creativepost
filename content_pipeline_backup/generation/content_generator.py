class ContentGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    async def generate_content(self, topic, style, tone):
        """Generate content based on the given parameters."""
        return {
            "text": f"Generated content about {topic} in {style} style with {tone} tone",
            "metadata": {
                "topic": topic,
                "style": style,
                "tone": tone
            }
        }
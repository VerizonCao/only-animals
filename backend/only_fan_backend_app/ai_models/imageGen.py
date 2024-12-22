import openai
from typing import Optional
from pathlib import Path
import os
from datetime import datetime



class ImageGenerator:
    """A class to handle AI image generation using OpenAI's DALL-E model."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the ImageGenerator with an API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Please provide it either through the constructor or set it as an environment variable 'OPENAI_API_KEY'")
        openai.api_key = self.api_key

    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        model: str = "dall-e-3",
        n: int = 1
    ) -> str:
        """
        Generate an image based on the provided prompt.

        Args:
            prompt (str): The description of the image to generate
            size (str): Image size (e.g., "1024x1024")
            model (str): The model to use (e.g., "dall-e-3")
            n (int): Number of images to generate

        Returns:
            str: URL of the generated image
        """
        try:
            response = openai.images.generate(
                model=model,
                prompt=prompt,
                n=n,
                size=size
            )
            
            # Return the URL of the first generated image
            print(response.data[0].url)
            return response.data[0].url
            
        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")

# Example usage:
if __name__ == "__main__":
    # For testing purposes
    generator = ImageGenerator()
    prompt = "A yellow cute dog wear black glasses and white t-shirt, is flying a kite now"
    image_url = generator.generate_image(prompt)
    print(f"Generated Image URL: {image_url}")

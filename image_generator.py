#!/usr/bin/env python3
"""
Image Generator for Story Generator

This module handles the generation of images for stories using OpenAI API.
"""

import os
import json
import base64
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from prompts import IMAGE_PROMPT_BREAKDOWN, CREATE_IMAGE_PROMPTS_SCHEMA
from config import API_KEY_ENV_VAR, IMAGES_DIR


class ImageGenerator:
    """Handles the generation of images using OpenAI API.
    
    Args:
        model: OpenAI model for image generation to be used
        nb_images: number of images to generate for the story
        size: size of the images
        target_age: target age group for the story
        api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
    """

    def __init__(self, image_model: str = "gpt-image-1", text_model: str = "gpt-4.1", nb_images: int = 1, size: str = "1024x1024", target_age: int = 3, story_content: str = "", api_key: Optional[str] = None):
        self.image_model = image_model
        self.text_model = text_model
        self.nb_images = nb_images
        self.size = size
        self.target_age = target_age
        self.story_content = story_content
        
        load_dotenv()
        self.api_key = os.getenv(API_KEY_ENV_VAR)
        if not self.api_key:
            raise ValueError(f"OpenAI API key is required. Set {API_KEY_ENV_VAR} environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def get_image_prompts(self):
        """Get the image prompts for the nb_images selected for the story by calling OpenAI text API to break down the story content into nb_images prompts"""
        
        prompt = IMAGE_PROMPT_BREAKDOWN.format(
            nb_images=self.nb_images,
            target_age=self.target_age,
            story_content=self.story_content
        )
        
        # Use function schema from prompts module
        function_schema = CREATE_IMAGE_PROMPTS_SCHEMA
        
        response = self.client.chat.completions.create(
            model=self.text_model,
            messages=[{"role": "user", "content": prompt}],
            tools=[function_schema],
            tool_choice={"type": "function", "function": {"name": "create_image_prompts_table"}},
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract the function call response
        tool_call = response.choices[0].message.tool_calls[0]
        image_prompts_data = json.loads(tool_call.function.arguments)
        
        return image_prompts_data
            
    def generate_image(self, image_number: int, prompt: str):
        """Generate an image based on the prompt."""
        image = self.client.images.generate(
            model = self.image_model,
            prompt = prompt,
            n = self.nb_images, 
            size = self.size,
            quality = "low"
        )

        # Decode the base64 image data
        image_bytes = base64.b64decode(image.data[0].b64_json)

        # Save the image as output.png
        with open(f"{IMAGES_DIR}/output_{image_number}.png", "wb") as f:
            f.write(image_bytes)

        return image_bytes 
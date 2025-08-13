#!/usr/bin/env python3
"""
Image Generator for Story Generator

This module handles the generation of images for stories using OpenAI API.
"""

import os
import json
import base64
import requests
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from story_prompts import IMAGE_PROMPT_BREAKDOWN, CREATE_IMAGE_PROMPTS_SCHEMA
from config import API_KEY_ENV_VAR, IMAGES_DIR
import fal_client


class ImageGenerator:
    """Handles the generation of images using OpenAI API.
    
    Args:
        image_model: OpenAI model for image generation to be used
        text_model: OpenAI model for text generation
        size: size of the images
        target_age: target age group for the story
        title: title of the story
        story_content: content of the story
        image_style: style of the images to generate
        api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
    """

    def __init__(self, image_model: str, text_model: str, nb_images: int, size: str, target_age: int, title: str, story_content: str, image_style: str, api_key: Optional[str]):
        self.image_model = image_model
        self.text_model = text_model
        self.nb_images = nb_images
        self.size = size
        self.target_age = target_age
        self.title = title
        self.story_content = story_content
        self.image_style = image_style
        
        load_dotenv()
        self.api_key = os.getenv(API_KEY_ENV_VAR)
        if not self.api_key:
            raise ValueError(f"OpenAI API key is required. Set {API_KEY_ENV_VAR} environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def get_image_prompts(self):
        """Get the image prompts for the nb_images selected for the story by calling OpenAI text API to break down the story content into nb_images prompts"""
        
        prompt = IMAGE_PROMPT_BREAKDOWN.format(
            total_images=self.nb_images + 2,  # +1 for title page + 1 for "The End" page
            nb_images=self.nb_images,
            target_age=self.target_age,
            title=self.title,
            story_content=self.story_content,
            image_style=self.image_style
        )
        
        # Use function schema from prompts module
        function_schema = CREATE_IMAGE_PROMPTS_SCHEMA
        
        response = self.client.chat.completions.create(
            model=self.text_model,
            messages=[{"role": "user", "content": prompt}],
            tools=[function_schema],
            tool_choice={"type": "function", "function": {"name": "create_image_prompts_table"}},
            temperature=0.7,
            max_tokens=32768
        )
    
        # Extract the function call response
        tool_call = response.choices[0].message.tool_calls[0]
        image_prompts_data = json.loads(tool_call.function.arguments)
        
        print(f"🔍 Image prompt generation tokens used: {response.usage.total_tokens} (input: {response.usage.prompt_tokens}, output: {response.usage.completion_tokens})")
        
        return image_prompts_data
            
    def generate_image(self, image_number: int, prompt: str, method: str):
        """Generate an image based on the prompt."""
        
        if method == "openai":
            print(f"🔍 Generating image {image_number} with OpenAI")
            
            # OpenAI image generation
            image = self.client.images.generate(
                model=self.image_model,
                prompt=prompt,
                n=1,  # Generate 1 image at a time
                size=self.size,
                quality="low"
            )
            
            # Decode the base64 image data
            image_bytes = base64.b64decode(image.data[0].b64_json)

            # Save the image
            with open(f"{IMAGES_DIR}/output_{image_number}.png", "wb") as f:
                f.write(image_bytes)

            return image_bytes
        
        elif method == "falai-openai":
            print(f"🔍 Generating image {image_number} with Fal AI and OpenAI")
            

            # Get OpenAI API key from environment
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
  
            result = fal_client.subscribe(
                self.image_model,
                arguments={
                    "prompt": prompt,
                    "openai_api_key": openai_api_key,
                    "size": self.size,
                    "number_of_images": 1,  # Generate 1 image at a time
                },
            )
            
            # Handle FAL AI response by downloading the image from the URL
            URL = result['images'][0]['url']
            print(f"🔍 Downloading from URL: {URL}")
            response = requests.get(URL)    
            image_bytes = response.content

            # Save the image
            with open(f"{IMAGES_DIR}/output_{image_number}.png", "wb") as f:
                f.write(image_bytes)

            return image_bytes 

        elif method == "falai-non-openai": 
            print(f"🔍 Generating image {image_number} with Fal AI with model {self.image_model}")
            
            result = fal_client.subscribe(
                self.image_model,
                arguments={
                    "prompt": prompt,
                    "size": self.size,
                    "number_of_images": 1,  # Generate 1 image at a time
                },
            )
            
            # Handle FAL AI response by downloading the image from the URL
            URL = result['images'][0]['url']
            print(f"🔍 Downloading from URL: {URL}")
            response = requests.get(URL)    
            image_bytes = response.content

            # Save the image
            with open(f"{IMAGES_DIR}/output_{image_number}.png", "wb") as f:
                f.write(image_bytes)

            return image_bytes

        else:
            print(f"❌ Image generation method {method} not supported")
            return None
            
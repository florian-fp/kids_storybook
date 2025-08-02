#!/usr/bin/env python3
"""
Children's Storybook Generator

This module generates age-appropriate children's stories using OpenAI's GPT-4 model.
"""

import os
from dotenv import load_dotenv
import requests

from openai import OpenAI
from openai import OpenAIError

import json

from typing import Dict, Optional
from dataclasses import dataclass

import base64

class StoryGenerator:
    """Handles the generation of children's stories using OpenAI API."""
    
    def __init__(self, model: str = "gpt-4.1", max_words: int = 150, reading_time_minutes: tuple = (2, 4), target_age: int = 3, api_key: Optional[str] = None):
        """
        Initialize the story generator.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
            model: OpenAI model to be used
            max_words: maximum number of words in the story
            reading_time_minutes: tuple of minimum and maximum reading time in minutes
            target_age: target age group for the story
        """

        self.model = "gpt-4.1"
        self.max_words = 150
        self.reading_time_minutes = (2, 4)
        self.target_age = 3

        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def _get_base_prompt(self) -> str:
        """Generate the base prompt for story creation."""

        return f"""
        Write a children's storybook for a {self.target_age}-year-old. The story should be:
        - Wholesome, imaginative, and age-appropriate
        - Written in simple yet rich language that is easy for a parent to read aloud
        - Maximum {self.max_words} words, to be read aloud in {self.reading_time_minutes[0]}-{self.reading_time_minutes[1]} minutes
        - Should include repetition, rhyme, and sound play when possible
        - Structured with clear beginning, middle, and end
        - Featuring a fun and relatable main character (like a talking animal, toy, or curious child)
        - Centered around an engaging and magical adventure that teaches a gentle life lesson (like kindness, courage, friendship, or curiosity)
        - Include vivid descriptions to inspire illustration ideas (e.g., "a glowing rainbow bridge made of jellybeans")
        - Add a short, one-sentence title and a 1–2 sentence summary at the beginning
        - Provide the output as a JSON with title, summary, and story content. Story content should only include the story, not the title or summary.
        """
    
    def generate_story(self, user_prompt: str) -> Dict[str, str]:
        """
        Generate a children's story based on configured parameters.
        
        Returns:
            Dictionary containing the generated story with title, summary, and content.
            
        Raises:
            OpenAIError: If there's an error with the OpenAI API call.
            ValueError: If the response format is invalid.
        """
        try:
            consolidated_prompt = (
                self._get_base_prompt() + 
                "\nMake sure this story includes the following:" + 
                user_prompt
            )
            
            # Define the function schema for structured output
            function_schema = {
                "type": "function",
                "function": {
                    "name": "create_story",
                    "description": "Create a children's story with title, summary, and content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "A short, catchy title for the story"
                            },
                            "summary": {
                                "type": "string", 
                                "description": "A brief 1-2 sentence summary of the story"
                            },
                            "story_content": {
                                "type": "string",
                                "description": "The full story content with paragraphs and formatting"
                            }
                        },
                        "required": ["title", "summary", "story_content"]
                    }
                }
            }
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": consolidated_prompt}
                ],
                tools=[function_schema],
                tool_choice={"type": "function", "function": {"name": "create_story"}},
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the function call response
            tool_call = response.choices[0].message.tool_calls[0]
            story_data = json.loads(tool_call.function.arguments)
            
            return story_data
        
        except OpenAIError as e:
            raise OpenAIError(f"Error generating story: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error during story generation: {e}")

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
        self.target_age = 3
        self.story_content = story_content
        
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
    

    def get_image_prompts(self):
        """Get the image prompts for the nb_images selected for the story by calling OpenAI text API to break down the story content into nb_images prompts"""
        
        prompt = f"""
        Break down the following story content into {self.nb_images} image prompts.
        
        # Guidelines:
        Each prompt needs to respect the following guidelines:
        - The images should capture evenly spaced moments of the story
        - The images should be consistent in style and across characters. E.g., if a story character is used in several pictures, this character should look like the same character even if in different situations.
        - Characters need to be described in details
        - Style of images should be appropriate for a {self.target_age}-year-old
        - Prompts need to be optimized for ChatGPT image generation
        
        # Story content: {self.story_content}
        """
        
        # Define the function schema for structured table output
        function_schema = {
            "type": "function",
            "function": {
                "name": "create_image_prompts_table",
                "description": "Create a table of image prompts for a children's story",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_prompts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "image_number": {
                                        "type": "integer",
                                        "description": "The sequential number of the image (1, 2, 3, etc.)"
                                    },
                                    "prompt": {
                                        "type": "string",
                                        "description": "Detailed image generation prompt optimized for ChatGPT"
                                    }
                                },
                                "required": ["image_number", "prompt"]
                            },
                            "description": f"Array of {self.nb_images} image prompts"
                        }
                    },
                    "required": ["image_prompts"]
                }
            }
        }
        
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
            
            
    def generate_image(self, prompt: str):
        """Generate an image based on the prompt."""
        image = self.client.images.generate(
            model = self.image_model,
            prompt = prompt,
            n = self.nb_images,
            size = self.size
        )

        # Decode the base64 image data
        image_bytes = base64.b64decode(image.data[0].b64_json)
        
        # Save the image as output.png
        with open("output.png", "wb") as f:
            f.write(image_bytes)

        return image_bytes

def main():

    try:
        # Generate a story
        USER_PROMPT = """
        - Main character: a little baby canary
        - Adventure or challenge: the canary wants to fly all the way to the top of North Beach tower
        - Where does the story take place: the city of San Francisco
        - Any special message or lesson: with determination, you can achieve anything you want in life
        """
        print("\n=== Story Generation ===\n")
        story_generator = StoryGenerator()
        story = story_generator.generate_story(USER_PROMPT)
        
        print("\n=== Successful Story Generation===\n")
        # print(f"Title:\n {story.get('title', 'Untitled')}\n")
        # print(f"Summary:\n {story.get('summary', 'No summary available')}\n")
        # print(f"Story content:\n {story.get('story_content', 'No story content available')}\n")

        # Generate images prompts
        print("\n=== Image Prompts Generation ===\n")
        image_generator = ImageGenerator(story_content=story.get('story_content', 'No story content available'), nb_images=4)
        image_prompts = image_generator.get_image_prompts()
        print("\n=== Successful Image Prompts Generation ===\n")
        # print("Image Prompts Table:")
        # for prompt_data in image_prompts.get('image_prompts', []):
        #     print(f"Image {prompt_data['image_number']}: {prompt_data['prompt']}")
        #     print("---")

        # # Generate images
        
        print("\n=== Image Generation ===\n")
        for image_prompt in image_prompts.get('image_prompts', []):
            print(f"Generating image {image_prompt.get('image_number', 'No image number available')}")
            print(f"Prompt: {image_prompt.get('prompt', 'No prompt available')}")
            image = image_generator.generate_image(image_prompt.get('prompt', 'No prompt available'))
        
        print(f"\n=== Successful Image Generation ===")

    except (ValueError, OpenAIError) as e:
        print(f"Error: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
       

if __name__ == "__main__":
    main()



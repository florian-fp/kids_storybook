#!/usr/bin/env python3
"""
Story and Image Generator - Orchestrates story and image generation
"""

from story_generator import StoryGenerator
from image_generator import ImageGenerator
from utils import add_rate_limiting_delay, create_error_output, create_success_output
from config import IMAGE_GENERATION_DELAY
from openai import OpenAIError


def generate_story_and_images(user_prompt, nb_images, text_model, max_words, reading_time_minutes, target_age, image_model, image_size):
    """
    Main function to generate story and images.
    
    Args:
        user_prompt (str): The user's story prompt
        nb_images (int): Number of images to generate
        text_model (str): OpenAI model for text generation
        max_words (int): Maximum words for the story
        reading_time_minutes (int): Reading time in minutes
        target_age (int): Target age group
        image_model (str): OpenAI model for image generation
        image_size (str): Size of generated images
    
    Returns:
        tuple: Formatted output for Gradio interface
    """
    try:
        print("\n=== NEW RUN ===\n")
        
        # Generate a story
        story_generator = StoryGenerator(
            model=text_model, 
            max_words=max_words, 
            reading_time_minutes=reading_time_minutes, 
            target_age=target_age
        )
        story = story_generator.generate_story(user_prompt=user_prompt)
    
        # Generate images prompts
        image_generator = ImageGenerator(
            image_model=image_model, 
            text_model=text_model, 
            nb_images=nb_images, 
            size=image_size, 
            target_age=target_age, 
            story_content=story.get('story_content', 'No story content available')
        )
        image_prompts = image_generator.get_image_prompts()
        image_prompts_list = [prompt_data.get('prompt', '') for prompt_data in image_prompts.get('image_prompts', [])]

        # Generate images
        for image_prompt in image_prompts.get('image_prompts', []):
            add_rate_limiting_delay(IMAGE_GENERATION_DELAY)  # Use configurable delay
            image_number = image_prompt.get('image_number', 1)
            image = image_generator.generate_image(
                image_number=image_number, 
                prompt=image_prompt.get('prompt', 'No prompt available')
            )

        # Return Gradio output using utility function
        return create_success_output(story, nb_images, image_prompts_list)

    except (ValueError, OpenAIError) as e:
        print(f"Error: {e}")
        return create_error_output(nb_images, str(e))
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return create_error_output(nb_images, str(e)) 
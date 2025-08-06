#!/usr/bin/env python3
"""
Story and Image Generator - Orchestrates story and image generation
"""

from story_generator import StoryGenerator
from image_generator import ImageGenerator
from utils import add_rate_limiting_delay, create_error_output, create_success_output, create_success_output_dictionnary
from config import IMAGE_GENERATION_DELAY, IMAGES_DIR, WORDS_PER_IMAGE_AGES_3_4, WORDS_PER_IMAGE_AGES_5_6, WORDS_PER_IMAGE_AGES_7_PLUS
from openai import OpenAIError
import os

def generate_story_and_images(user_prompt, text_model, max_words, target_age, image_model, image_size, output_format="gradio"):
    """
    Main function to generate story and images.
    
    Args:
        user_prompt (str): The user's story prompt
        text_model (str): OpenAI model for text generation
        max_words (int): Maximum words for the story
        target_age (int): Target age group
        image_model (str): OpenAI model for image generation
        image_size (str): Size of generated images
    
    Returns:
        tuple: Formatted output for Gradio interface or dictionnary for PDF generation
    """
    try:
        print(f"📚 Generating story and images for user prompt: {user_prompt}...")
        
        # Generate a story
        story_generator = StoryGenerator(
            model=text_model, 
            max_words=max_words, 
            target_age=target_age
        )
        story = story_generator.generate_story(user_prompt=user_prompt)
        print(f"✅ Story generated: '{story.get('title', 'Untitled')}'")
        
        # Calculate number of images based on story length and target age
        story_content = story.get('story_content', '')
        word_count = len(story_content.split())
        
        # Adjust words per image based on target age
        if target_age <= 4:
            words_per_image = WORDS_PER_IMAGE_AGES_3_4  # More images for younger children
        elif target_age <= 6:
            words_per_image = WORDS_PER_IMAGE_AGES_5_6  # Medium images for 5-6 year olds
        else:
            words_per_image = WORDS_PER_IMAGE_AGES_7_PLUS  # Fewer images for older children (7+)
        
        nb_images = max(1, word_count // words_per_image)
        print(f"📊 Story has {word_count} words. Generating {nb_images} content images with {words_per_image} words per image for target age {target_age}")
    
        # Generate images prompts
        image_generator = ImageGenerator(
            image_model=image_model, 
            text_model=text_model, 
            nb_images=nb_images, 
            size=image_size, 
            target_age=target_age, 
            title=story.get('title', 'Untitled'),
            story_content=story.get('story_content', 'No story content available')
        )
        image_prompts = image_generator.get_image_prompts()
        image_prompts_list = [prompt_data.get('prompt', '') for prompt_data in image_prompts.get('image_prompts', [])]


        # Store all images in a new image directory
        if os.path.exists(IMAGES_DIR):
            os.system(f"rm -rf {IMAGES_DIR}")
        
        os.makedirs(IMAGES_DIR, exist_ok=True)


        # Generate images
        for image_prompt in image_prompts.get('image_prompts', []):
            add_rate_limiting_delay(IMAGE_GENERATION_DELAY)  # Use configurable delay
            image_number = image_prompt.get('image_number', 1) - 1
            image = image_generator.generate_image(
                image_number=image_number, 
                prompt=image_prompt.get('prompt', 'No prompt available')
            )
        print(f"✅ {len(image_prompts_list)} images generated")

        if output_format == "gradio":
            # Return tuple useful for Gradio interface
            return create_success_output(story, nb_images, image_prompts_list)
        elif output_format == "dictionnary":
            # Return a dictionnary with the story, the images and the image prompts more useful for formatting purposes
            return create_success_output_dictionnary(story, nb_images, image_prompts_list)


    except (ValueError, OpenAIError) as e:
        print(f"Error: {e}")
        return create_error_output(1, str(e))  # Default to 1 image for error case
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return create_error_output(1, str(e))  # Default to 1 image for error case 
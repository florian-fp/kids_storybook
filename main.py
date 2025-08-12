#!/usr/bin/env python3
"""
Main entry point for the Children's Storybook Generator
"""

import sys
sys.path.append('gradio_interface')
sys.path.append('story_and_image_gen')
sys.path.append('book_format')

from interface import launch_interface
from story_and_image_generator import generate_story_and_images
from formatting import StorybookFormatter
from config import FORMAT_OPTIONS, TARGET_WORDS, TARGET_AGE, TEXT_MODEL, IMAGE_MODEL, IMAGE_SIZE, IMAGE_STYLE

if __name__ == "__main__":
    # 1. Gradio interface - useful for reviewing story and images
    # launch_interface() 

    # # 2. PDF generation - useful for reviewing final formating 


    USER_PROMPT = """
        - Main character: a young boy
        - Supporting characters: a golden retriever pup
        - Setting: in San Francisco
        - Plot elements: young boy is visiting San Francisco with his golden retriever pup who is acting as a guide
        - Tone & Style: fun, adventurous, and heartwarming
        - Language: simple and easy to understand
        - Vocabulary: simple and easy to understand
        - Lesson: friendship and adventure
    """
    story_dict = generate_story_and_images(USER_PROMPT, TEXT_MODEL, TARGET_WORDS, TARGET_AGE, IMAGE_MODEL, IMAGE_SIZE, IMAGE_STYLE, "", output_format="dictionary", image_generation_method="openai")
    
    # # Test data in dictionary format
    # story_dict = {
    #     "title": "Sunny Pup and Splashy Seal's San Francisco Day",
    #     "summary": "whatever",
    #     "story_content": "Sunny pup bounces, tail goes swish! Splashy seal claps, 'Let's go, I wish!' \n \n Over the Golden Gate, wag and wiggle—\nDown to Fisherman's Wharf, giggle, giggle!\n\nRolling, splashing, under blue sky,\nChasing fog, watching boats go by.\n\nSunny and Splashy, side by side,\nAdventure is fun, with friends as your guide!",
    #     "images": ["images/output_0.png", "images/output_1.png", "images/output_2.png", "images/output_3.png"]
    # }

    formatter = StorybookFormatter(story_dict, FORMAT_OPTIONS)
    formatter.build_storybook()
    

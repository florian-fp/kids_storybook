#!/usr/bin/env python3
"""
Main entry point for the Children's Storybook Generator
"""

from interface import launch_interface
from story_and_image_generator import generate_story_and_images
from formatting import StorybookFormatter
from config import FORMAT_OPTIONS, MAX_WORDS, TARGET_AGE, TEXT_MODEL, IMAGE_MODEL, IMAGE_SIZE

if __name__ == "__main__":
    # 1. Gradio interface - useful for reviewing story and images
    # launch_interface() 

    # 2. PDF generation - useful for reviewing final formating 

    USER_PROMPT = "A story about a rhino who wants to be a giraffe"
    
    # Test data in dictionary format
    # story_dict = {
    #     "title": "Benny the Bubble's Adventure",
    #     "summary": "A magical bubble learns to fly and explore the world",
    #     "story_content": "Benny the bubble was born in a bathtub. He was small, shiny, and full of dreams. \"I want to fly!\" he said with a giggle. A gentle breeze carried him out the window, over trees, rooftops, and a surprised cat! \"Wheee!\" Benny sang, swirling with butterflies and dancing with dandelions. But POP!—a bird nearly bumped him. \"Careful!\" Benny laughed, bouncing higher. As the sun began to set, Benny sparkled like a tiny rainbow. Finally, he gently landed on a little girl's nose. She giggled, and Benny smiled, proud to have flown so far. And with a pop, he was gone.",
    #     "images": ["images/output_0.png", "images/output_1.png", "images/output_2.png", "images/output_3.png", "images/output_4.png", "images/output_5.png"]
    # }

    story_dict = generate_story_and_images(USER_PROMPT, TEXT_MODEL, MAX_WORDS, TARGET_AGE, IMAGE_MODEL, IMAGE_SIZE, output_format="dictionnary")
    # print(f"story_dict: {story_dict}")

    formatter = StorybookFormatter(story_dict, FORMAT_OPTIONS)
    formatter.build_storybook()

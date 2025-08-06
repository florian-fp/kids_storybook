#!/usr/bin/env python3
"""
Utility functions for the Story Generator
"""

import time
from typing import List, Tuple
from openai import OpenAIError
from config import IMAGE_GENERATION_DELAY


def add_rate_limiting_delay(seconds: int = IMAGE_GENERATION_DELAY):
    """Add delay to respect API rate limits."""
    time.sleep(seconds)


def create_error_output(nb_images: int, error_message: str) -> Tuple:
    """Create standardized error output for the interface."""
    error_output = ["Error occurred", "Error occurred", "Error occurred"]
    for i in range(nb_images):
        error_output.append(None)  # No image
        error_output.append(f"Error: {error_message}")  # Error message as prompt
    return tuple(error_output)


def create_success_output(story: dict, nb_images: int, image_prompts_list: List[str]) -> Tuple:
    """Create standardized success output for the interface."""
    output = [
        story.get("title", "Untitled"),
        story.get("summary", "No summary available"),
        story.get("story_content", "No story content available")
    ]
    
    # Add image outputs (title + content + "The End" page)
    for i in range(nb_images + 2):  # +2 for title page and "The End" page
        output.append(f"images/output_{i}.png")  # Image path (0-based indexing)
        output.append(image_prompts_list[i] if i < len(image_prompts_list) else "No prompt available")  # Prompt text
    print(f"output: {output}")
    return tuple(output) 


def create_success_output_dictionnary(story: dict, nb_images: int, image_prompts_list: List[str]) -> dict:
    """Create standardized success output for the interface."""
    output = story.copy()
    output['images'] = [f"images/output_{i}.png" for i in range(nb_images+2)]  # +2 for title and "The End" pages
    return output
#!/usr/bin/env python3
"""
Gradio Interface for Story Generator
"""

import gradio as gr
from config import (
    MAX_WORDS, TARGET_AGE, TEXT_MODEL, NB_IMAGES_MAX, IMAGE_MODEL, IMAGE_SIZE
)
import sys
sys.path.append('../story_and_image_gen')
from story_and_image_generator import generate_story_and_images

def generate_story_and_images_gradio(user_prompt, text_model, max_words, target_age, image_model, image_size):
    """Generate story and images for the Gradio interface."""
    result = generate_story_and_images(user_prompt, text_model, max_words, target_age, image_model, image_size, output_format="gradio")
    
    # Ensure we return the correct number of outputs for the interface
    # The interface expects: 3 story outputs + (NB_IMAGES_MAX+2) * 2 image outputs (title + content + "The End")
    expected_outputs = 3 + (NB_IMAGES_MAX + 2) * 2
    
    if len(result) < expected_outputs:
        # Pad with None values if we don't have enough outputs
        result = list(result) + [None] * (expected_outputs - len(result))
    elif len(result) > expected_outputs:
        # Truncate if we have too many outputs
        result = result[:expected_outputs]
    
    return result

def create_interface():
    """Create and configure the Gradio interface."""
    
    demo = gr.Interface(
        fn=generate_story_and_images_gradio,
        inputs=[
            gr.Textbox(label="User Prompt", placeholder="Describe what you would like to see in your story", lines=4),
            gr.Dropdown(label="Text Model", choices=["gpt-4.1", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"], value=TEXT_MODEL),
            gr.Slider(label="Max Words", value=MAX_WORDS, minimum=50, maximum=1500, step=50),
            gr.Slider(label="Target Age", value=TARGET_AGE, minimum=3, maximum=8, step=1),
            gr.Dropdown(label="Image Model", choices=["gpt-image-1", "dall-e-3", "dall-e-2"], value=IMAGE_MODEL),
            gr.Dropdown(label="Image Size", choices=["1024x1536", "1024x1024", "1536x1024", "auto"], value=IMAGE_SIZE),
        ],
        outputs=[
            gr.Textbox(label="Title", interactive=False),
            gr.Textbox(label="Summary", interactive=False, lines=2),
            gr.Textbox(label="Story Content", interactive=False, lines=8),
        ] + [component for i in range(NB_IMAGES_MAX+2) for component in [
            gr.Image(label=f"Generated Image {i}"),
            gr.Textbox(label=f"Image Prompt {i}", interactive=False, lines=2)
        ]],
        title="Children's Story Generator"
    )
    
    return demo


def launch_interface():
    """Launch the Gradio interface."""
    interface = create_interface()
    interface.launch() 
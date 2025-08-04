#!/usr/bin/env python3
"""
Gradio Interface for Story Generator
"""

import gradio as gr
from config import (
    MAX_WORDS, READING_TIME_MINUTES, TARGET_AGE, TEXT_MODEL,
    NB_IMAGES, IMAGE_MODEL, IMAGE_SIZE
)
from story_and_image_generator import generate_story_and_images


def create_interface():
    """Create and configure the Gradio interface."""
    
    demo = gr.Interface(
        fn=generate_story_and_images,
        inputs=[
            gr.Textbox(label="USER_PROMPT", placeholder="Describe what you would like to see in your story", lines=4),
            gr.Number(label="Number of Images", value=NB_IMAGES, minimum=1, maximum=5, step=1),
            gr.Textbox(label="Text Model", value=TEXT_MODEL),
            gr.Number(label="Max Words", value=MAX_WORDS),
            gr.Number(label="Reading Time Minutes", value=READING_TIME_MINUTES),
            gr.Number(label="Target Age", value=TARGET_AGE),
            gr.Textbox(label="Image Model", value=IMAGE_MODEL),
            gr.Textbox(label="Image Size", value=IMAGE_SIZE),
        ],
        outputs=[
            gr.Textbox(label="Title", interactive=False),
            gr.Textbox(label="Summary", interactive=False, lines=2),
            gr.Textbox(label="Story", interactive=False, lines=8),
        ] + [component for i in range(NB_IMAGES) for component in [
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
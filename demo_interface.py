import gradio as gr
from story_generator import StoryGenerator, ImageGenerator
import os

def story_generator_fn(user_prompt, image_prompt):
    story_generator = StoryGenerator()
    story_data = story_generator.generate_story(user_prompt)

    image_generator = ImageGenerator()
    image_generator.generate_image(image_prompt)
    
    return story_data.get("title", "Untitled"), story_data.get("summary", "No summary available"), story_data.get("story_content", "No story content available"), "output.png"

demo = gr.Interface(
    fn=story_generator_fn,
    inputs=[
        gr.Textbox(label="Story Requirements", placeholder="Describe your story requirements...", lines=4),
        gr.Textbox(label="Image Prompt", placeholder="Describe the image you want to generate...", lines=2)
    ],
    outputs=[
        gr.Textbox(label="Title", interactive=False),
        gr.Textbox(label="Summary", interactive=False, lines=2),
        gr.Textbox(label="Story", interactive=False, lines=8),
        gr.Image(label="Generated Image")
    ],
    title="Children's Story Generator"
)

demo.launch()
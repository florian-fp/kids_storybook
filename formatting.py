#!/usr/bin/env python3
"""
Story and Image Formatting - Takes story text and image output and turns it into a formatted PDF storybook 
"""

from story_and_image_generator import generate_story_and_images
import re
from jinja2 import Template
from weasyprint import HTML
import os

import webbrowser
from config import IMAGE_GENERATION_DELAY, IMAGE_MODEL, IMAGE_SIZE, MAX_WORDS, READING_TIME_MINUTES, TARGET_AGE, TEXT_MODEL, NB_IMAGES, HTML_DIR, PDF_DIR
from prompts import STORY_STANDARD_TEMPLATE

class StorybookFormatter:
    def __init__(self, story_dict, nb_pages, format_options):
        self.story_dict = story_dict
        self.nb_pages = nb_pages
        self.format_options = format_options

    def break_story_into_pages(self):
        """
        Break the story text into N_PAGES = N_IMAGES

        PB: we loose the original punctuation, needs to be improved with a GPT4.1 call instead of this regex rule   
        
        Returns:
            story_pages: dictionary of page_number: page_content
        """
        story_pages = {}
        
        # Split the story text into sentences
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(sentence_pattern, self.story_dict['story_content'])
        nb_sentences_per_page = round(len(sentences) / self.nb_pages)

        for page_number in range(self.nb_pages-1):
            # Evenly split the sentences across the pages
            page_sentences = sentences[page_number * nb_sentences_per_page:(page_number + 1) * nb_sentences_per_page]
            page_content = {
                'text': '. '.join(page_sentences),
                'image': self.story_dict['images'][page_number]
            }
            story_pages[page_number] = page_content

        story_pages[self.nb_pages-1] = {
            'text': '. '.join(sentences[(self.nb_pages-1) * nb_sentences_per_page:]),
            'image': self.story_dict['images'][self.nb_pages-1]
        }

        # print(f"Broke down story text into: {len(story_pages)} pages")
        return story_pages

    def build_html(self, story_pages):
        """Build HTML for all pages

        Args:
            story_pages: dictionary of page_number: page_content

        Returns:
            None
        """

        rendered_pages = []
        template = Template(STORY_STANDARD_TEMPLATE)

        # Store all HTML rendered pages in a directory
        if os.path.exists(HTML_DIR):
            os.system(f"rm -rf {HTML_DIR}")
            # print(f"Deleted existing directory: {HTML_DIR}")
        
        os.makedirs(HTML_DIR, exist_ok=True)
        # print(f"Created new directory: {HTML_DIR}")

        for page_number in sorted(story_pages.keys()):

            # Render HTML for each page
            content = story_pages[page_number]
            page_html = template.render(
                text=content['text'], 
                image=content['image'], 
                page_width=self.format_options['page_size_width'], 
                page_height=self.format_options['page_size_height']
            )
            rendered_pages.append(page_html)
            # print(f"Page {page_number} rendered with HTML")

            with open(f"{HTML_DIR}/storybook_html_page_{page_number+1}.html", 'w', encoding='utf-8') as f:
                f.write(page_html)
    
    def build_pdf(self):
        """Build PDF for all pages

        Args:
            None

        Returns:
            None
        """
        # Store all PDF rendered pages in a directory
        if os.path.exists(PDF_DIR):
            os.system(f"rm -rf {PDF_DIR}")
            # print(f"Deleted existing directory: {PDF_DIR}")
        
        os.makedirs(PDF_DIR, exist_ok=True)
        # print(f"Created new directory: {PDF_DIR}")

        for page_number in range(self.nb_pages):
            try:
                # Read the HTML file content
                html_file_path = f"{HTML_DIR}/storybook_html_page_{page_number+1}.html"
                with open(html_file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Generate PDF from HTML content
                HTML(string=html_content, base_url=os.getcwd()).write_pdf(
                    f"{PDF_DIR}/storybook_pdf_page_{page_number+1}.pdf",
                    stylesheets=[],
                    presentational_hints=True
                )
                print(f"PDF saved to {PDF_DIR}/storybook_pdf_page_{page_number+1}.pdf")

            except Exception as e:
                print(f"Error creating PDF: {e}")
                return False

    def build_storybook(self):
        """Build the storybook
        
        Args:
            None
        
        Returns:
            None
        """

        # Break down story into pages
        story_pages = self.break_story_into_pages()

        # Build HTML of each page
        self.build_html(story_pages)
        
        # # Convert HTML to PDF
        self.build_pdf()

        print(f"Storybook built")


def test():
    """Test the StorybookFormatter with sample data"""
    
    # Test data in dictionary format
    story_dict = {
        "title": "Benny the Bubble's Adventure",
        "summary": "A magical bubble learns to fly and explore the world",
        "story_content": "Benny the bubble was born in a bathtub. He was small, shiny, and full of dreams. \"I want to fly!\" he said with a giggle. A gentle breeze carried him out the window, over trees, rooftops, and a surprised cat! \"Wheee!\" Benny sang, swirling with butterflies and dancing with dandelions. But POP!—a bird nearly bumped him. \"Careful!\" Benny laughed, bouncing higher. As the sun began to set, Benny sparkled like a tiny rainbow. Finally, he gently landed on a little girl's nose. She giggled, and Benny smiled, proud to have flown so far. And with a pop, he was gone.",
        "images": ["images/output_1.png", "images/output_2.png", "images/output_3.png", "images/output_4.png", "images/output_5.png"]
    }
    
    NB_PAGES = 5
    
    # Import format options from config
    from config import FORMAT_OPTIONS

    # Create formatter and build storybook
    formatter = StorybookFormatter(story_dict, NB_PAGES, FORMAT_OPTIONS)
    formatter.build_storybook()


if __name__ == "__main__":
    test()
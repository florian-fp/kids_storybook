#!/usr/bin/env python3
"""
Story and Image Formatting - Takes story text and image output and turns it into a formatted PDF storybook 
"""


import re
from jinja2 import Template
from weasyprint import HTML
import os

import webbrowser
from config import IMAGE_GENERATION_DELAY, IMAGE_MODEL, IMAGE_SIZE, MAX_WORDS, TARGET_AGE, TEXT_MODEL, NB_IMAGES_MAX, HTML_DIR, PDF_DIR
from prompts import STORY_STANDARD_TEMPLATE, STORY_TITLE_TEMPLATE

# Try to import PyPDF2 for PDF merging, fallback to pypdf if not available
try:
    from PyPDF2 import PdfMerger
except ImportError:
    try:
        from pypdf import PdfMerger
    except ImportError:
        PdfMerger = None

class StorybookFormatter:
    def __init__(self, story_dict, format_options, nb_pages=None):
        self.story_dict = story_dict
        self.format_options = format_options
        
        # Calculate nb_pages from the number of images if not provided
        if nb_pages is None:
            # Number of pages = number of images - 2 (excluding title and "The End" pages)
            total_images = len(self.story_dict.get('images', []))
            self.nb_pages = total_images - 2
            print(f"📄 Calculated {self.nb_pages} content pages from {total_images} total images (title + content + 'The End')")
        else:
            self.nb_pages = nb_pages

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
        
        if len(sentences) % self.nb_pages == 0:
            nb_sentences_per_page = (round(len(sentences) / self.nb_pages))
        else:
            nb_sentences_per_page = (round(len(sentences) / self.nb_pages)) + 1

        # Create the title page
        title_page_content = {
            'text': self.story_dict['title'],
            'image': self.story_dict['images'][0]
        }
        story_pages[0] = title_page_content

        # Create each page content
        for page_number in range(1, self.nb_pages+1):
            # Evenly split the sentences across the pages
            page_sentences = sentences[(page_number-1) * nb_sentences_per_page:(page_number) * nb_sentences_per_page]
            page_content = {
                'text': '. '.join(page_sentences),
                'image': self.story_dict['images'][page_number]
            }
            story_pages[page_number] = page_content
        
        # Add the "The End" page
        end_page_content = {
            'text': 'The End',
            'image': self.story_dict['images'][self.nb_pages+1]
        }
        story_pages[self.nb_pages+1] = end_page_content

        return story_pages

    def build_html(self, story_pages):
        """Build HTML for all pages

        Args:
            story_pages: dictionary of page_number: page_content

        Returns:
            None
        """

        rendered_pages = []

        # Store all HTML rendered pages in a directory
        if os.path.exists(HTML_DIR):
            os.system(f"rm -rf {HTML_DIR}")
        
        os.makedirs(HTML_DIR, exist_ok=True)

        # Create the title page
        page_number = 0
        content = story_pages[page_number]
        template_title = Template(STORY_TITLE_TEMPLATE)
        page_html = template_title.render(
            text=content['text'], 
            image=content['image'],
            page_width=self.format_options['page_size_width'], 
            page_height=self.format_options['page_size_height']
        )
        rendered_pages.append(page_html)
        
        # Save title page
        with open(f"{HTML_DIR}/storybook_html_page_{page_number}.html", 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"Title page saved to {HTML_DIR}/storybook_html_page_{page_number}.html")

        # Create the main story pages
        for page_number in sorted(story_pages.keys()):
            if page_number == 0:  # Skip title page, already handled
                continue
            
            content = story_pages[page_number]
            
            # Regular content page
            template_standard = Template(STORY_STANDARD_TEMPLATE)
            page_html = template_standard.render(
                text=content['text'], 
                image=content['image'],
                page_width=self.format_options['page_size_width'], 
                page_height=self.format_options['page_size_height']
            )
            
            rendered_pages.append(page_html)
            
            with open(f"{HTML_DIR}/storybook_html_page_{page_number}.html", 'w', encoding='utf-8') as f:
                f.write(page_html)
            if page_number == self.nb_pages + 1:  # "The End" page
                print(f"Creating 'The End' page with text: {content['text']}")
            print(f"Page {page_number} saved to {HTML_DIR}/storybook_html_page_{page_number}.html")
    
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
        
        os.makedirs(PDF_DIR, exist_ok=True)

        for page_number in range(self.nb_pages+2):  # +2 for title and "The End" pages
            try:
                HTML(string=f"{HTML_DIR}/storybook_html_page_{page_number}.html", base_url=os.getcwd()).write_pdf(
                    f"{PDF_DIR}/storybook_pdf_page_{page_number}.pdf",
                    stylesheets=[],
                    presentational_hints=True
                )

            except Exception as e:
                print(f"Error creating PDF: {e}")
                return False

    def merge_pdfs(self, output_filename="storybook.pdf"):
        """Merge individual PDF pages into a single storybook PDF
        
        Args:
            output_filename: Name of the output merged PDF file
        
        Returns:
            bool: True if successful, False otherwise
        """         
        try:
            merger = PdfMerger()
            
            # Add each page PDF to the merger
            for page_number in range(self.nb_pages+2):  # +2 for title and "The End" pages
                pdf_path = f"{PDF_DIR}/storybook_pdf_page_{page_number}.pdf"
                if os.path.exists(pdf_path):
                    merger.append(pdf_path)
                else:
                    print(f"Warning: Page {page_number} PDF not found at {pdf_path}")
            
            # Write the merged PDF
            output_path = f"{PDF_DIR}/{output_filename}"
            merger.write(output_path)
            merger.close()
            
            return True
            
        except Exception as e:
            print(f"Error merging PDFs: {e}")
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
        
        # Convert HTML to PDF
        self.build_pdf()
        
        # Merge individual PDFs into a single storybook
        self.merge_pdfs()

        print(f"✅ Storybook PDF generated")


    
#!/usr/bin/env python3
"""
Configuration file for the Children's Storybook Generator
"""

# Story generation settings
TARGET_WORDS = 50
TARGET_AGE = 3
TEXT_MODEL = "gpt-4.1"  # only OpenAI models are supported for now

# Image generation settings
NB_IMAGES_MAX = 15
IMAGE_MODEL = "gpt-image-1"
# IMAGE_MODEL = "fal-ai/gpt-image-1/text-to-image/byok"
# IMAGE_MODEL = "fal-ai/ideogram/character"
IMAGE_SIZE = "1024x1024"
IMAGE_STYLE = 'watercolor children\'s book illustration'  # Default image style for children's books

# Age-based words per image settings
WORDS_PER_IMAGE_AGES_3_4 = 25    # More images for younger children (3-4 years)
WORDS_PER_IMAGE_AGES_5_6 = 40    # Medium images for 5-6 year olds
WORDS_PER_IMAGE_AGES_7_PLUS = 75  # Fewer images for older children (7+ years)

# Storybook formatting settings (converted to pixels at 96 DPI)
FORMAT_OPTIONS = {
    "page_size_width": "1024px",  # 8.5 inches * 96 DPI  
    "page_size_height": "1024px",  # 11 inches * 96 DPI
}

# API settings
API_KEY_ENV_VAR = "OPENAI_API_KEY"

# Rate limiting settings (in seconds)
IMAGE_GENERATION_DELAY = 2  # Delay between image API calls to avoid rate limits

# File paths
IMAGES_DIR = "images"
HTML_DIR = "html"
PDF_DIR = "pdf"
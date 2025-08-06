#!/usr/bin/env python3
"""
Configuration file for the Children's Storybook Generator
"""

# Story generation settings
MAX_WORDS = 200
TARGET_AGE = 3
TEXT_MODEL = "gpt-4.1"  # only OpenAI models are supported for now

# Image generation settings
NB_IMAGES_MAX = 15
IMAGE_MODEL = "gpt-image-1"  # only OpenAI models are supported for now
IMAGE_SIZE = "1024x1024"

# Age-based words per image settings
WORDS_PER_IMAGE_AGES_3_4 = 25    # More images for younger children (3-4 years)
WORDS_PER_IMAGE_AGES_5_6 = 50    # Medium images for 5-6 year olds
WORDS_PER_IMAGE_AGES_7_PLUS = 75  # Fewer images for older children (7+ years)

# Storybook formatting settings
FORMAT_OPTIONS = {
    "page_size_width": "8.5in",
    "page_size_height": "11in",
}

# API settings
API_KEY_ENV_VAR = "OPENAI_API_KEY"

# Rate limiting settings (in seconds)
IMAGE_GENERATION_DELAY = 2  # Delay between image API calls to avoid rate limits

# File paths
IMAGES_DIR = "images"
HTML_DIR = "html"
PDF_DIR = "pdf"
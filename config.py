#!/usr/bin/env python3
"""
Configuration file for the Children's Storybook Generator
"""

# Story generation settings
MAX_WORDS = 500
READING_TIME_MINUTES = 5
TARGET_AGE = 3
TEXT_MODEL = "gpt-4.1"  # only OpenAI models are supported for now

# Image generation settings
NB_IMAGES = 10
IMAGE_MODEL = "gpt-image-1"  # only OpenAI models are supported for now
IMAGE_SIZE = "1024x1024"

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
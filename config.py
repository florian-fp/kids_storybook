#!/usr/bin/env python3
"""
Configuration file for the Children's Storybook Generator
"""

# Story generation settings
MAX_WORDS = 500
READING_TIME_MINUTES = 10
TARGET_AGE = 5
TEXT_MODEL = "gpt-4.1"  # only OpenAI models are supported for now

# Image generation settings
NB_IMAGES = 5
IMAGE_MODEL = "gpt-image-1"  # only OpenAI models are supported for now
IMAGE_SIZE = "1024x1024"

# API settings
API_KEY_ENV_VAR = "OPENAI_API_KEY"

# Rate limiting settings (in seconds)
IMAGE_GENERATION_DELAY = 60  # Delay between image API calls to avoid rate limits

# File paths
IMAGES_DIR = "images" 
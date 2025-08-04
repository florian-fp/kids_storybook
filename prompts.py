#!/usr/bin/env python3
"""
Simple prompt storage for Story Generator
"""

# Story generation prompts
STORY_BASE_PROMPT = """
Write a children's storybook for a {target_age}-year-old. The story should be:
- Wholesome, imaginative, and age-appropriate
- Written in simple yet rich language that is easy for a parent to read aloud
- Maximum {max_words} words, to be read aloud in approximately {reading_time_minutes} minutes
- Should include repetition, rhyme, and sound play when possible
- Structured with clear beginning, middle, and end
- Featuring a fun and relatable main character (like a talking animal, toy, or curious child)
- Centered around an engaging and magical adventure that teaches a gentle life lesson (like kindness, courage, friendship, or curiosity)
- Include vivid descriptions to inspire illustration ideas (e.g., "a glowing rainbow bridge made of jellybeans")
- Add a short, one-sentence title and a 1–2 sentence summary at the beginning
- Provide the output as a JSON with title, summary, and story content. Story content should only include the story, not the title or summary.
"""

USER_PROMPT_TEMPLATE = "Make sure this story includes the following: {user_prompt}"

# Image generation prompts
IMAGE_PROMPT_BREAKDOWN = """
Break down the following story content into {nb_images} image prompts.

# Guidelines:
Each prompt needs to respect the following guidelines:
- The images should capture evenly spaced moments of the story
- The images should be consistent in style and across characters. E.g., if a story character is used in several pictures, this character should look like the same character even if in different situations.
- Characters need to be described in details
- Style of images should be appropriate for a {target_age}-year-old
- Prompts need to be optimized for ChatGPT image generation

# Story content: {story_content}
"""

# Function schemas
CREATE_STORY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "create_story",
        "description": "Create a children's story with title, summary, and content",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "A short, catchy title for the story"
                },
                "summary": {
                    "type": "string",
                    "description": "A brief 1-2 sentence summary of the story"
                },
                "story_content": {
                    "type": "string",
                    "description": "The full story content with paragraphs and formatting"
                }
            },
            "required": ["title", "summary", "story_content"]
        }
    }
}

CREATE_IMAGE_PROMPTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "create_image_prompts_table",
        "description": "Create a table of image prompts for a children's story",
        "parameters": {
            "type": "object",
            "properties": {
                "image_prompts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "image_number": {
                                "type": "integer",
                                "description": "The sequential number of the image (1, 2, 3, etc.)"
                            },
                            "prompt": {
                                "type": "string",
                                "description": "Detailed image generation prompt optimized for ChatGPT"
                            }
                        },
                        "required": ["image_number", "prompt"]
                    },
                    "description": "Array of {nb_images} image prompts"
                }
            },
            "required": ["image_prompts"]
        }
    }
} 
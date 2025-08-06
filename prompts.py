#!/usr/bin/env python3
"""
Simple prompt storage for Story Generator
"""

# Story generation prompts
STORY_BASE_PROMPT = """
Write a children's storybook for a {target_age}-year-old. The story should be:
- Wholesome, imaginative, and age-appropriate
- Written in simple yet rich language that is easy for a parent to read aloud
- Maximum {max_words} words
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
Break down the following story content into {total_images} image prompts. The first image prompt is for the title page and the other {nb_images} image prompts are for the story content.

# Guidelines:
Each prompt needs to respect the following guidelines:
- The images should capture evenly spaced moments of the story
- The images should be consistent in style and across characters. E.g., if a story character is used in several pictures, this character should look like the same character even if in different situations.
- Characters need to be described in details
- Style of images should be appropriate for a {target_age}-year-old
- Prompts need to be optimized for ChatGPT image generation

# Story title: {title}
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

# Standard page HTML template
STORY_STANDARD_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: {{ page_width }} {{ page_height }};
                margin: 0;
            }
            
            body {
                width: {{ page_width }};
                height: {{ page_height }};
                margin: 0;
                padding: 0;
                font-family: "Comic Sans MS", "Arial Rounded MT Bold", "Arial", sans-serif;
                box-sizing: border-box;
                page-break-after: always;
                position: relative;
                overflow: hidden;
            }

            .page-container {
                width: 100%;
                height: 100%;
                position: relative;
                background-color: #f0f8ff; /* Light blue background fallback */
            }

            .background-image {
                width: 100%;
                height: 100%;
                object-fit: cover;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
            }

            .text-overlay {
                position: absolute;
                bottom: 1.5in;
                left: 1in;
                right: 1in;
                background: rgba(255, 255, 255, 0.95);
                padding: 0.75in;
                border-radius: 0.5in;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                z-index: 2;
                border: 3px solid #ff6b6b;
            }

            .text {
                font-size: 24px;
                line-height: 1.4;
                color: #2c3e50;
                text-align: center;
                font-weight: bold;
                margin: 0;
                text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
            }

            /* Fallback for when no image is provided */
            .no-image {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="page-container">
            {% if image %}
            <img src="{{ image }}" class="background-image" alt="Story illustration" />
            {% else %}
            <div class="no-image">
                <div>No image available</div>
            </div>
            {% endif %}
            
            {% if text %}
            <div class="text-overlay">
                <div class="text">{{ text }}</div>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """

# Title page HTML template for kid's book cover
STORY_TITLE_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: {{ page_width }} {{ page_height }};
                margin: 0;
            }
            
            body {
                width: {{ page_width }};
                height: {{ page_height }};
                margin: 0;
                padding: 0;
                font-family: "Comic Sans MS", "Arial Rounded MT Bold", "Arial", sans-serif;
                box-sizing: border-box;
                page-break-after: always;
                position: relative;
                overflow: hidden;
            }

            .page-container {
                width: 100%;
                height: 100%;
                position: relative;
                background-color: #f0f8ff; /* Light blue background fallback */
            }

            .background-image {
                width: 100%;
                height: 100%;
                object-fit: cover;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
            }

            .title-overlay {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(255, 255, 255, 0.95);
                padding: 1.5in;
                border-radius: 0.75in;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
                z-index: 2;
                border: 5px solid #ff6b6b;
                text-align: center;
                min-width: 60%;
            }

            .title-text {
                font-size: 36px;
                line-height: 1.2;
                color: #2c3e50;
                text-align: center;
                font-weight: bold;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.9);
                letter-spacing: 1px;
            }

            .title-decoration {
                position: absolute;
                top: -10px;
                left: -10px;
                right: -10px;
                bottom: -10px;
                border: 3px dashed #ffd93d;
                border-radius: 0.75in;
                z-index: -1;
            }

            /* Fallback for when no image is provided */
            .no-image {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="page-container">
            {% if image %}
            <img src="{{ image }}" class="background-image" alt="Story illustration" />
            {% else %}
            <div class="no-image">
                <div>No image available</div>
            </div>
            {% endif %}
            
            {% if text %}
            <div class="title-overlay">
                <div class="title-decoration"></div>
                <div class="title-text">{{ text }}</div>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
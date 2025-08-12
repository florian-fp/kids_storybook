#!/usr/bin/env python3
"""
Simple prompt storage for Story Generator
"""

# Story generation prompts
STORY_BASE_PROMPT = """
Write a children's storybook for a {target_age}-year-old. The story should be:
- Wholesome, imaginative, and age-appropriate
- Written in simple yet rich language that is easy for a parent to read aloud
- Length should be {target_words} words
- Should include repetition, rhyme, and sound play when possible
- Structured with clear beginning, middle, and end
- Featuring a fun and relatable main character (like a talking animal, toy, or curious child)
- Centered around an engaging and magical adventure that teaches a gentle life lesson (like kindness, courage, friendship, or curiosity)
- Include vivid descriptions to inspire illustration ideas
- Genereate a short, one-sentence title and a 1–2 sentence summary at the beginning
- Provide the output as a JSON with title, summary, and story content. Story content should only include the story, not the title or summary.
"""

USER_PROMPT_TEMPLATE = "This story should include the following: {user_prompt}"

# Image generation prompts
IMAGE_PROMPT_BREAKDOWN = """

Break down the following story into {total_images} distinct image prompts:
- The 1st prompt is for the title page.
- The next {nb_images} prompts are for the story scenes.
- The final prompt is for The End page.

# STEP 1 — CREATE CHARACTER SHEET
Before writing any scene prompts, identify all recurring characters in the story and create a Character Sheet entry for each. 
For each character, describe them in **rich, fixed detail** including:
    - Age (or apparent age)
    - Gender (if applicable)
    - Ethnicity/skin tone (if applicable)
    - Hair style/color (if applicable)
    - Eye color (if applicable)
    - Distinguishing features (e.g., freckles, clothing, accessories)
    - Fixed personality traits or facial expressions (e.g., always cheerful, always curious)
    - Any special features for non-human characters (e.g., exact color pattern of feathers or fur, beak/eye shape, wing/tail details, etc.)
    - **Important**: This description must be written so it can be **copied verbatim** into every prompt without changes.

# STEP 2 — PROMPT STRUCTURE FOR EACH IMAGE
For each image prompt:
1. **Character description**  
   - Paste the *exact same* wording from the Character Sheet for each recurring character present in the scene.  
   - Do not paraphrase, shorten, or alter the description in any way.
2. **Character pose**  
   - Describe the specific pose(s) of the character(s) in the scene.
3. **Scene description**  
   - Describe in detail the setting, background, and objects in the scene.
4. **Image style**  
   - The image is drawn in {image_style} style appropriate for a {target_age}-year-old.  
   - Keep color palette, line work, and mood identical across all images.

# STEP 3 — SPECIAL PAGES
- **Title Page**: Show main character(s) in a visually appealing, introductory pose with the story’s title prominently displayed in a fitting style.  
- **The End Page**: A celebratory, happy ending scene that visually communicates the resolution of the story (e.g., smiling characters, warm colors, peaceful setting).

# STORY DATA
Title: {title}
Content: {story_content}

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

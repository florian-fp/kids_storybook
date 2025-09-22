#!/usr/bin/env python3
"""
FastAPI Backend for Kids Storybook Generator Web Interface
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
root_dir = parent_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "story_and_image_gen"))

from story_and_image_gen.story_and_image_generator import generate_story_and_images
from config import (
    TARGET_WORDS, TARGET_AGE, TEXT_MODEL, IMAGE_MODEL, IMAGE_SIZE, 
    IMAGE_STYLE, IMAGE_GENERATION_METHOD, IMAGES_DIR
)

app = FastAPI(title="Kids Storybook Generator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

images_path = Path(parent_dir) / IMAGES_DIR
images_path.mkdir(exist_ok=True)

app.mount("/images", StaticFiles(directory=str(images_path)), name="images")

class StoryRequest(BaseModel):
    user_prompt: str
    text_model: str = TEXT_MODEL
    target_words: int = TARGET_WORDS
    target_age: int = TARGET_AGE
    image_model: str = IMAGE_MODEL
    image_size: str = IMAGE_SIZE
    image_style: str = IMAGE_STYLE
    custom_style_text: Optional[str] = ""
    image_generation_method: str = IMAGE_GENERATION_METHOD

class StoryResponse(BaseModel):
    title: str
    summary: str
    story_content: str
    images: List[str]
    image_prompts: List[str]
    success: bool
    error_message: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Kids Storybook Generator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/config")
async def get_config():
    """Get available configuration options for the story generator."""
    return {
        "text_models": ["gpt-4.1", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        "image_models": ["fal-ai/flux/dev", "dall-e-3", "dall-e-2"],
        "image_sizes": ["1024x1536", "1024x1024", "1536x1024", "auto"],
        "image_styles": [
            "watercolor children's book illustration",
            "cartoon style",
            "realistic illustration", 
            "artistic painting",
            "minimalist design",
            "digital art",
            "hand-drawn sketch",
            "3D rendered"
        ],
        "image_generation_methods": ["openai", "falai-non-openai", "falai-openai"],
        "defaults": {
            "text_model": TEXT_MODEL,
            "target_words": TARGET_WORDS,
            "target_age": TARGET_AGE,
            "image_model": IMAGE_MODEL,
            "image_size": IMAGE_SIZE,
            "image_style": IMAGE_STYLE,
            "image_generation_method": IMAGE_GENERATION_METHOD
        },
        "ranges": {
            "target_words": {"min": 50, "max": 1500, "step": 50},
            "target_age": {"min": 3, "max": 8, "step": 1}
        }
    }

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story_endpoint(request: StoryRequest):
    """Generate a children's story with images based on the provided parameters."""
    try:
        # Use custom style text if provided, otherwise use the dropdown value
        final_image_style = request.custom_style_text.strip() if request.custom_style_text and request.custom_style_text.strip() else request.image_style
        
        result = generate_story_and_images(
            user_prompt=request.user_prompt,
            text_model=request.text_model,
            target_words=request.target_words,
            target_age=request.target_age,
            image_model=request.image_model,
            image_size=request.image_size,
            image_style=final_image_style,
            custom_style_text="",
            output_format="dictionary",
            image_generation_method=request.image_generation_method
        )
        
        if isinstance(result, dict):
            image_files = []
            if 'images' in result:
                for img_path in result['images']:
                    if os.path.exists(img_path):
                        filename = os.path.basename(img_path)
                        image_files.append(f"/images/{filename}")
            
            return StoryResponse(
                title=result.get('title', 'Untitled'),
                summary=result.get('summary', 'No summary available'),
                story_content=result.get('story_content', 'No story content available'),
                images=image_files,
                image_prompts=result.get('image_prompts', []),
                success=True
            )
        else:
            raise ValueError("Unexpected result format from story generation")
        
    except Exception as e:
        print(f"Error generating story: {e}")
        return StoryResponse(
            title="Error",
            summary="An error occurred",
            story_content="Failed to generate story",
            images=[],
            image_prompts=[],
            success=False,
            error_message=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#!/usr/bin/env python3
"""
Children's Storybook Generator

This module generates age-appropriate children's stories using OpenAI's GPT-4 model.
"""

import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from prompts import STORY_BASE_PROMPT, USER_PROMPT_TEMPLATE, CREATE_STORY_SCHEMA
from config import API_KEY_ENV_VAR
from utils import add_rate_limiting_delay, create_error_output, create_success_output

class StoryGenerator:
    """Handles the generation of children's stories using OpenAI API."""
    
    def __init__(self, model: str = "gpt-4.1", max_words: int = 150, target_age: int = 3, api_key: Optional[str] = None):
        """
        Initialize the story generator.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
            model: OpenAI model to be used
            max_words: maximum number of words in the story
            target_age: target age group for the story
        """

        self.model = model
        self.max_words = max_words
        self.target_age = target_age
        
        # No prompt manager needed - using simple imports

        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def _get_base_prompt(self) -> str:
        """Generate the base prompt for story creation."""
        return STORY_BASE_PROMPT.format(
            target_age=self.target_age,
            max_words=self.max_words
        )
    
    def generate_story(self, user_prompt: str) -> Dict[str, str]:
        """
        Generate a children's story based on configured parameters.
        
        Returns:
            Dictionary containing the generated story with title, summary, and content.
            
        Raises:
            OpenAIError: If there's an error with the OpenAI API call.
            ValueError: If the response format is invalid.
        """
        try:
            consolidated_prompt = (
                self._get_base_prompt() + 
                "\n" + USER_PROMPT_TEMPLATE.format(user_prompt=user_prompt)
            )
            
            # Use function schema from prompts module
            function_schema = CREATE_STORY_SCHEMA
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": consolidated_prompt}
                ],
                tools=[function_schema],
                tool_choice={"type": "function", "function": {"name": "create_story"}},
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the function call response
            tool_call = response.choices[0].message.tool_calls[0]
            story_data = json.loads(tool_call.function.arguments)
            
            return story_data
        
        except OpenAIError as e:
            raise OpenAIError(f"Error generating story: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error during story generation: {e}")
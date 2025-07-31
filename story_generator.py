#!/usr/bin/env python3
"""
Children's Storybook Generator

This module generates age-appropriate children's stories using OpenAI's GPT-4 model.
"""

import os
from dotenv import load_dotenv

from openai import OpenAI
from openai import OpenAIError

import json

from typing import Dict, Optional
from dataclasses import dataclass


class StoryGenerator:
    """Handles the generation of children's stories using OpenAI API."""
    
    def __init__(self, model: str = "gpt-4.1", max_words: int = 150, reading_time_minutes: tuple = (2, 4), target_age: int = 3, api_key: Optional[str] = None):
        """
        Initialize the story generator.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
            model: OpenAI model to be used
            max_words: maximum number of words in the story
            reading_time_minutes: tuple of minimum and maximum reading time in minutes
            target_age: target age group for the story
        """

        self.model = "gpt-4.1"
        self.max_words = 150
        self.reading_time_minutes = (2, 4)
        self.target_age = 3

        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def _get_base_prompt(self) -> str:
        """Generate the base prompt for story creation."""

        return f"""
        Write a children's storybook for a {self.target_age}-year-old. The story should be:
        - Wholesome, imaginative, and age-appropriate
        - Written in simple yet rich language that is easy for a parent to read aloud
        - Maximum {self.max_words} words, to be read aloud in {self.reading_time_minutes[0]}-{self.reading_time_minutes[1]} minutes
        - Should include repetition, rhyme, and sound play when possible
        - Structured with clear beginning, middle, and end
        - Featuring a fun and relatable main character (like a talking animal, toy, or curious child)
        - Centered around an engaging and magical adventure that teaches a gentle life lesson (like kindness, courage, friendship, or curiosity)
        - Include vivid descriptions to inspire illustration ideas (e.g., "a glowing rainbow bridge made of jellybeans")
        - Add a short, one-sentence title and a 1–2 sentence summary at the beginning
        - Provide the output as a JSON with title, summary, and story
        """
    
    def _get_user_prompt(self) -> str:
        """Generate the user-specific prompt with story requirements."""
        
        return """
        - Main character: a little baby canary
        - Adventure or challenge: the canary wants to fly all the way to the top of North Beach tower
        - Where does the story take place: the city of San Francisco
        - Any special message or lesson: with determination, you can achieve anything you want in life
        """
    
    def generate_story(self) -> Dict[str, str]:
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
                "\nMake sure this story includes the following:" + 
                self._get_user_prompt()
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": consolidated_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the response content
            story_text = response.choices[0].message.content
            
            # Try to parse as JSON, fallback to plain text if needed
            try:
                story_data = json.loads(story_text)
                return story_data
            except json.JSONDecodeError:
                # If not JSON, return as plain text
                return {
                    "title": "Generated Story",
                    "summary": "A magical children's story",
                    "story": story_text
                }
                
        except OpenAIError as e:
            raise OpenAIError(f"Error generating story: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error during story generation: {e}")


def main():
    """Main function to demonstrate story generation."""
    try:
        # Initialize the story generator
        generator = StoryGenerator()
        
        # Generate the story
        story = generator.generate_story()
        
        # Print the results
        print("Generated Story:")
        print("=" * 50)
        print(f"Title: {story.get('title', 'Untitled')}")
        print(f"Summary: {story.get('summary', 'No summary available')}")
        print("\nStory:")
        print(story.get('story', 'No story content available'))
        
    except (ValueError, OpenAIError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()



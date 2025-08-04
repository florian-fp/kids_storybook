# Children's Storybook Generator

A modular Python application that generates children's stories with AI-generated images using OpenAI's API.

## 🏗️ Project Structure

```
kids_storybook/
├── main.py                 # Entry point - launches the interface
├── story_generator.py      # Story generation logic (StoryGenerator class)
├── story_and_image_generator.py  # Orchestration logic (coordinates story + images)
├── image_generator.py      # Image generation logic
├── prompts.py             # Prompt templates
├── config.py              # Configuration and constants
├── interface.py           # Gradio interface setup
├── utils.py               # Utility functions
└── README.md              # This file
```

## 📁 File Descriptions

### **`main.py`**
- Simple entry point that launches the Gradio interface
- Just imports and calls the interface launcher

### **`story_generator.py`**
- Contains the `StoryGenerator` class only
- Handles story generation using OpenAI's text API
- Uses prompts from `prompts.py`

### **`story_and_image_generator.py`**
- Contains the `generate_story_and_images` function
- Orchestrates story and image generation
- Coordinates between StoryGenerator and ImageGenerator

### **`image_generator.py`**
- Contains the `ImageGenerator` class
- Handles image generation using OpenAI's image API
- Manages image prompts and file saving

### **`prompts.py`**
- Contains all prompt templates as Python constants
- Includes function schemas for OpenAI API calls
- Easy to modify without touching core logic

### **`config.py`**
- All configuration constants in one place
- Easy to modify settings like model names, image counts, etc.
- Includes rate limiting configuration (`IMAGE_GENERATION_DELAY`)
- Centralized configuration management

### **`interface.py`**
- Gradio interface setup and configuration
- Handles user input and output formatting
- Separates UI concerns from business logic

### **`utils.py`**
- Common utility functions
- Rate limiting helpers
- Error handling and output formatting

## 🚀 Usage

### **Quick Start**
```bash
# Install dependencies
pip install openai gradio python-dotenv

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the application
python main.py
```

### **Configuration**
Edit `config.py` to modify:
- Number of images to generate
- Target age group
- Story length
- Model settings

### **Custom Prompts**
Edit `prompts.py` to modify:
- Story generation prompts
- Image prompt templates
- Function schemas

### **Rate Limiting**
Edit `config.py` to adjust:
- `IMAGE_GENERATION_DELAY`: Delay between image API calls (default: 15 seconds)
- Helps avoid OpenAI API rate limits


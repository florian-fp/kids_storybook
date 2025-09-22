# Children's Storybook Generator

A modular Python application that generates children's stories with AI-generated images using OpenAI's API.

## 🏗️ Project Structure

```
kids_storybook/
├── main.py                 # Entry point - launches interfaces
├── story_and_image_gen/    # Core story generation modules
│   ├── story_generator.py      # Story generation logic (StoryGenerator class)
│   ├── story_and_image_generator.py  # Orchestration logic (coordinates story + images)
│   ├── image_generator.py      # Image generation logic
│   └── story_prompts.py        # Prompt templates
├── gradio_interface/       # Original Gradio interface
│   └── interface.py           # Gradio interface setup
├── web_interface/          # New web interface
│   ├── backend/               # FastAPI backend
│   │   ├── main.py               # API server
│   │   ├── requirements.txt      # Python dependencies
│   │   └── .env                  # Environment variables
│   ├── frontend/              # React frontend
│   │   ├── src/                  # Source code
│   │   ├── package.json          # Node.js dependencies
│   │   └── vite.config.ts        # Build configuration
│   └── README.md              # Web interface documentation
├── book_format/            # PDF generation
├── config.py              # Configuration and constants
├── utils.py               # Utility functions
└── README.md              # This file
```

## 📁 File Descriptions

### **`main.py`**
- Entry point that can launch either Gradio or web interface
- Use `--interface gradio` for the original interface
- Use `--interface web` for the new modern web interface

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

### **`gradio_interface/interface.py`**
- Original Gradio interface setup and configuration
- Handles user input and output formatting
- Simple auto-generated UI

### **`web_interface/`**
- Modern web interface with React frontend and FastAPI backend
- Responsive design with Tailwind CSS
- RESTful API architecture
- Enhanced user experience with loading states and error handling

### **`utils.py`**
- Common utility functions
- Rate limiting helpers
- Error handling and output formatting

## 🚀 Usage

### **Quick Start**

#### Option 1: Gradio Interface (Default)
```bash
# Install dependencies
pip install openai gradio python-dotenv

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the Gradio interface
python main.py
# or explicitly
python main.py --interface gradio
```

#### Option 2: Web Interface (New!)
```bash
# Install Python dependencies
pip install -r web_interface/backend/requirements.txt

# Install Node.js dependencies (first time only)
cd web_interface/frontend && npm install && cd ../..

# Set your API keys
export OPENAI_API_KEY="your-api-key-here"
export FAL_KEY="your-fal-api-key-here"  # Optional

# Launch the web interface
python main.py --interface web
```

The web interface will automatically:
- Start the FastAPI backend server on http://localhost:8000
- Start the React frontend server on http://localhost:3000  
- Open your browser to the web interface

### **Interface Comparison**

| Feature | Gradio Interface | Web Interface |
|---------|------------------|---------------|
| Setup | Simple | Requires Node.js |
| UI/UX | Basic | Modern & Responsive |
| Customization | Limited | Highly Customizable |
| Performance | Good | Optimized |
| Mobile Support | Basic | Full Responsive |
| Deployment | Gradio Cloud | Any Web Host |

### **Configuration**
Edit `config.py` to modify:
- Number of images to generate
- Target age group
- Story length
- Model settings

### **Image Style Options**
The interface provides multiple image style options:
- **Predefined Styles**: Choose from styles like "watercolor children's book illustration", "cartoon style", "realistic illustration", etc.
- **Custom Style**: Always visible text input where you can type your own style description (e.g., "oil painting in the style of Van Gogh")

### **Custom Prompts**
Edit `prompts.py` to modify:
- Story generation prompts
- Image prompt templates
- Function schemas

### **Rate Limiting**
Edit `config.py` to adjust:
- `IMAGE_GENERATION_DELAY`: Delay between image API calls (default: 15 seconds)
- Helps avoid OpenAI API rate limits


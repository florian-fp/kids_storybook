# Kids Storybook Generator - Web Interface

A modern web interface for generating children's stories with AI-generated illustrations.

## Features

- Interactive web form with all story generation parameters
- Real-time story generation with progress indicators
- Beautiful display of generated stories and images
- Responsive design that works on desktop and mobile
- Modern React frontend with TypeScript
- FastAPI backend integrated with existing story generation modules

## Architecture

### Backend (FastAPI)
- **Location**: `web_interface/backend/`
- **Main file**: `main.py`
- **Features**:
  - RESTful API endpoints for story generation
  - Integration with existing story generation modules
  - Static file serving for generated images
  - CORS enabled for frontend communication

### Frontend (React + TypeScript)
- **Location**: `web_interface/frontend/`
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Build tool**: Vite
- **Features**:
  - Interactive form with all story parameters
  - Real-time story display
  - Image gallery for generated illustrations
  - Loading states and error handling

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key
- FAL AI API key (optional, for alternative image generation)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd web_interface/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. Start the backend server:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd web_interface/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   
   The web interface will be available at `http://localhost:3000`

## API Endpoints

### GET /config
Returns available configuration options for the story generator.

### POST /generate-story
Generates a story based on the provided parameters.

**Request body**:
```json
{
  "user_prompt": "A story about a brave little mouse",
  "text_model": "gpt-4o",
  "target_words": 200,
  "target_age": 5,
  "image_model": "fal-ai/flux/dev",
  "image_size": "1024x1024",
  "image_style": "watercolor children's book illustration",
  "custom_style_text": "",
  "image_generation_method": "falai-non-openai"
}
```

**Response**:
```json
{
  "title": "The Brave Little Mouse",
  "summary": "A heartwarming tale of courage...",
  "story_content": "Once upon a time...",
  "images": ["/images/image_1.png", "/images/image_2.png"],
  "image_prompts": ["A brave mouse...", "The mouse exploring..."],
  "success": true
}
```

### GET /images/{filename}
Serves generated image files.

## Development

### Building for Production

1. Build the frontend:
   ```bash
   cd web_interface/frontend
   npm run build
   ```

2. The built files will be in `frontend/dist/`

3. Configure the backend to serve the built frontend files for production deployment.

## Integration with Existing Code

The web interface integrates seamlessly with the existing story generation modules:

- Uses the same `generate_story_and_images` function from `story_and_image_generator.py`
- Respects all configuration settings from `config.py`
- Maintains compatibility with existing image generation methods
- Preserves all functionality from the original Gradio interface

## Comparison with Gradio Interface

| Feature | Gradio Interface | Web Interface |
|---------|------------------|---------------|
| User Interface | Auto-generated | Custom React components |
| Styling | Basic Gradio theme | Modern Tailwind CSS |
| Responsiveness | Limited | Fully responsive |
| Customization | Limited | Highly customizable |
| Integration | Standalone | Can be embedded/deployed |
| Performance | Good | Optimized for web |

## Troubleshooting

### Common Issues

1. **CORS errors**: Make sure the backend CORS settings allow requests from the frontend URL
2. **Image not loading**: Check that the images directory exists and has proper permissions
3. **API connection failed**: Verify the backend is running on the correct port
4. **Story generation timeout**: Increase the timeout in the frontend API configuration

### Logs

- Backend logs: Check the console where you started the FastAPI server
- Frontend logs: Check the browser developer console
- API errors: Check the Network tab in browser developer tools

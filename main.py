#!/usr/bin/env python3
"""
Main entry point for the Children's Storybook Generator
"""

import sys
import argparse
sys.path.append('gradio_interface')
sys.path.append('story_and_image_gen')
sys.path.append('book_format')

from interface import launch_interface
from story_and_image_generator import generate_story_and_images
from formatting import StorybookFormatter
from config import FORMAT_OPTIONS, TARGET_WORDS, TARGET_AGE, TEXT_MODEL, IMAGE_MODEL, IMAGE_SIZE, IMAGE_STYLE, IMAGE_GENERATION_METHOD

def launch_web_interface():
    """Launch the web interface (FastAPI backend + React frontend)"""
    import subprocess
    import os
    import time
    import webbrowser
    from pathlib import Path
    
    web_interface_dir = Path(__file__).parent / "web_interface"
    backend_dir = web_interface_dir / "backend"
    frontend_dir = web_interface_dir / "frontend"
    
    print("🚀 Starting Kids Storybook Generator Web Interface...")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found. Please ensure the web interface is properly set up.")
        return
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found. Please ensure the web interface is properly set up.")
        return
    
    try:
        print("📡 Starting backend server...")
        backend_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)
        
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        print("🎨 Starting frontend server...")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(5)
        
        print("✅ Web interface is starting up!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("\n🌟 Opening web interface in your browser...")
        
        webbrowser.open("http://localhost:3000")
        
        print("\n⚠️  Press Ctrl+C to stop both servers")
        
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ Servers stopped")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting web interface: {e}")
    except FileNotFoundError as e:
        print(f"❌ Required dependency not found: {e}")
        print("💡 Make sure Node.js and npm are installed for the frontend")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kids Storybook Generator")
    parser.add_argument(
        "--interface", 
        choices=["gradio", "web"], 
        default="gradio",
        help="Choose the interface to launch (default: gradio)"
    )
    
    args = parser.parse_args()
    
    if args.interface == "web":
        launch_web_interface()
    else:
        # 1. Gradio interface - useful for reviewing story and images
        launch_interface() 

    # # 2. PDF generation - useful for reviewing final formating 


    USER_PROMPT = """
        - Main character: a young boy
        - Supporting characters: a golden retriever pup
        - Setting: in San Francisco
        - Plot elements: young boy is visiting San Francisco with his golden retriever pup who is acting as a guide
        - Tone & Style: fun, adventurous, and heartwarming
        - Language: simple and easy to understand
        - Vocabulary: simple and easy to understand
        - Lesson: friendship and adventure
    """
    story_dict = generate_story_and_images(USER_PROMPT, TEXT_MODEL, TARGET_WORDS, TARGET_AGE, IMAGE_MODEL, IMAGE_SIZE, IMAGE_STYLE, "", "dictionary", IMAGE_GENERATION_METHOD)
    
    
    # Test data in dictionary format
    # story_dict = {
    #     "title": "Sunny Pup and Splashy Seal's San Francisco Day",
    #     "summary": "whatever",
    #     "story_content": "Sunny pup bounces, tail goes swish! Splashy seal claps, 'Let's go, I wish!' \n \n Over the Golden Gate, wag and wiggle—\nDown to Fisherman's Wharf, giggle, giggle!\n\nRolling, splashing, under blue sky,\nChasing fog, watching boats go by.\n\nSunny and Splashy, side by side,\nAdventure is fun, with friends as your guide!",
    #     "images": ["images/output_0.png", "images/output_1.png", "images/output_2.png", "images/output_3.png"]
    # }

    formatter = StorybookFormatter(story_dict, FORMAT_OPTIONS)
    formatter.build_storybook()
    

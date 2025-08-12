#!/usr/bin/env python3
"""
Simple prompt storage for Story Generator
"""


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
                bottom: 1in;
                left: 0.5in;
                right: 0.5in;
                background: rgba(255, 255, 255, 0.7);
                padding: 0.5in;
                border-radius: 0.5in;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                z-index: 2;
                border: 3px solid #87CEEB;
                backdrop-filter: blur(2px);
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


    # "The End" page HTML template

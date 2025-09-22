export interface StoryRequest {
  user_prompt: string;
  text_model: string;
  target_words: number;
  target_age: number;
  image_model: string;
  image_size: string;
  image_style: string;
  custom_style_text?: string;
  image_generation_method: string;
}

export interface StoryResponse {
  title: string;
  summary: string;
  story_content: string;
  images: string[];
  image_prompts: string[];
  success: boolean;
  error_message?: string;
}

export interface Config {
  text_models: string[];
  image_models: string[];
  image_sizes: string[];
  image_styles: string[];
  image_generation_methods: string[];
  defaults: {
    text_model: string;
    target_words: number;
    target_age: number;
    image_model: string;
    image_size: string;
    image_style: string;
    image_generation_method: string;
  };
  ranges: {
    target_words: { min: number; max: number; step: number };
    target_age: { min: number; max: number; step: number };
  };
}

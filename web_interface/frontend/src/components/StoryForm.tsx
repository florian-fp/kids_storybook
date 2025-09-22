import React, { useState, useEffect } from 'react';
import { StoryRequest, Config } from '../types';

interface StoryFormProps {
  onSubmit: (request: StoryRequest) => void;
  loading: boolean;
}

const StoryForm: React.FC<StoryFormProps> = ({ onSubmit, loading }) => {
  const [config, setConfig] = useState<Config | null>(null);
  const [formData, setFormData] = useState<StoryRequest>({
    user_prompt: '',
    text_model: '',
    target_words: 100,
    target_age: 5,
    image_model: '',
    image_size: '',
    image_style: '',
    custom_style_text: '',
    image_generation_method: ''
  });

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await fetch('/api/config');
        const configData = await response.json();
        setConfig(configData);
        setFormData(prev => ({
          ...prev,
          text_model: configData.defaults.text_model,
          target_words: configData.defaults.target_words,
          target_age: configData.defaults.target_age,
          image_model: configData.defaults.image_model,
          image_size: configData.defaults.image_size,
          image_style: configData.defaults.image_style,
          image_generation_method: configData.defaults.image_generation_method
        }));
      } catch (error) {
        console.error('Failed to fetch config:', error);
      }
    };

    fetchConfig();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.user_prompt.trim()) {
      alert('Please enter a story prompt');
      return;
    }
    onSubmit(formData);
  };

  const handleInputChange = (field: keyof StoryRequest, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (!config) {
    return <div className="text-center">Loading configuration...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Create Your Story</h2>
      
      {/* User Prompt */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Story Prompt
        </label>
        <textarea
          value={formData.user_prompt}
          onChange={(e) => handleInputChange('user_prompt', e.target.value)}
          placeholder="Describe what you would like to see in your story"
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      {/* Text Model */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Text Model
        </label>
        <select
          value={formData.text_model}
          onChange={(e) => handleInputChange('text_model', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {config.text_models.map(model => (
            <option key={model} value={model}>{model}</option>
          ))}
        </select>
      </div>

      {/* Target Words */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Words: {formData.target_words}
        </label>
        <input
          type="range"
          min={config.ranges.target_words.min}
          max={config.ranges.target_words.max}
          step={config.ranges.target_words.step}
          value={formData.target_words}
          onChange={(e) => handleInputChange('target_words', parseInt(e.target.value))}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>{config.ranges.target_words.min}</span>
          <span>{config.ranges.target_words.max}</span>
        </div>
      </div>

      {/* Target Age */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Age: {formData.target_age} years
        </label>
        <input
          type="range"
          min={config.ranges.target_age.min}
          max={config.ranges.target_age.max}
          step={config.ranges.target_age.step}
          value={formData.target_age}
          onChange={(e) => handleInputChange('target_age', parseInt(e.target.value))}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>{config.ranges.target_age.min}</span>
          <span>{config.ranges.target_age.max}</span>
        </div>
      </div>

      {/* Image Model */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Image Model
        </label>
        <select
          value={formData.image_model}
          onChange={(e) => handleInputChange('image_model', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {config.image_models.map(model => (
            <option key={model} value={model}>{model}</option>
          ))}
        </select>
      </div>

      {/* Image Size */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Image Size
        </label>
        <select
          value={formData.image_size}
          onChange={(e) => handleInputChange('image_size', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {config.image_sizes.map(size => (
            <option key={size} value={size}>{size}</option>
          ))}
        </select>
      </div>

      {/* Image Style */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Image Style
        </label>
        <select
          value={formData.image_style}
          onChange={(e) => handleInputChange('image_style', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {config.image_styles.map(style => (
            <option key={style} value={style}>{style}</option>
          ))}
        </select>
      </div>

      {/* Custom Style */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Custom Style (Optional)
        </label>
        <textarea
          value={formData.custom_style_text}
          onChange={(e) => handleInputChange('custom_style_text', e.target.value)}
          placeholder="Leave empty to use the selected style above, or type your own custom style description here..."
          rows={2}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Image Generation Method */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Image Generation Method
        </label>
        <select
          value={formData.image_generation_method}
          onChange={(e) => handleInputChange('image_generation_method', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {config.image_generation_methods.map(method => (
            <option key={method} value={method}>{method}</option>
          ))}
        </select>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full py-3 px-4 rounded-md text-white font-medium ${
          loading 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500'
        }`}
      >
        {loading ? 'Generating Story...' : 'Generate Story'}
      </button>
    </form>
  );
};

export default StoryForm;

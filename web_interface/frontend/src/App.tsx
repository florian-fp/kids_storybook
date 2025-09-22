import React, { useState } from 'react';
import StoryForm from './components/StoryForm';
import StoryDisplay from './components/StoryDisplay';
import { StoryRequest, StoryResponse } from './types';
import { generateStory } from './api';

function App() {
  const [story, setStory] = useState<StoryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateStory = async (request: StoryRequest) => {
    setLoading(true);
    setError(null);
    setStory(null);

    try {
      const response = await generateStory(request);
      setStory(response);
    } catch (err) {
      console.error('Error generating story:', err);
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Kids Storybook Generator
          </h1>
          <p className="text-gray-600">
            Create magical stories with AI-generated illustrations for children
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Story Form */}
          <div>
            <StoryForm onSubmit={handleGenerateStory} loading={loading} />
          </div>

          {/* Story Display */}
          <div>
            <StoryDisplay story={story} loading={loading} error={error} />
          </div>
        </div>

        <footer className="text-center mt-12 text-gray-500">
          <p>Powered by OpenAI and modern web technologies</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

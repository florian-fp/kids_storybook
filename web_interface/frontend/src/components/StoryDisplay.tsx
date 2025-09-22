import React from 'react';
import { StoryResponse } from '../types';
import { getImageUrl } from '../api';

interface StoryDisplayProps {
  story: StoryResponse | null;
  loading: boolean;
  error: string | null;
}

const StoryDisplay: React.FC<StoryDisplayProps> = ({ story, loading, error }) => {
  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Generating your story... This may take a few minutes.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 p-6 rounded-lg">
        <h3 className="text-red-800 font-medium mb-2">Error</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!story) {
    return (
      <div className="bg-gray-50 p-6 rounded-lg shadow-lg text-center">
        <p className="text-gray-600">Your generated story will appear here...</p>
      </div>
    );
  }

  if (!story.success) {
    return (
      <div className="bg-red-50 border border-red-200 p-6 rounded-lg">
        <h3 className="text-red-800 font-medium mb-2">Generation Failed</h3>
        <p className="text-red-600">{story.error_message || 'An unknown error occurred'}</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-3xl font-bold text-gray-800 mb-2">{story.title}</h2>
      </div>

      {/* Summary */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Summary</h3>
        <p className="text-gray-600 bg-gray-50 p-4 rounded-md">{story.summary}</p>
      </div>

      {/* Story Content */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Story</h3>
        <div className="text-gray-800 leading-relaxed bg-gray-50 p-4 rounded-md whitespace-pre-wrap">
          {story.story_content}
        </div>
      </div>

      {/* Images */}
      {story.images && story.images.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Generated Images</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {story.images.map((imagePath, index) => (
              <div key={index} className="space-y-2">
                <img
                  src={getImageUrl(imagePath)}
                  alt={`Story illustration ${index + 1}`}
                  className="w-full h-64 object-cover rounded-lg shadow-md"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIG5vdCBhdmFpbGFibGU8L3RleHQ+PC9zdmc+';
                  }}
                />
                {story.image_prompts && story.image_prompts[index] && (
                  <p className="text-sm text-gray-600 italic">
                    {story.image_prompts[index]}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default StoryDisplay;

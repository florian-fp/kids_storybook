import axios from 'axios';
import { StoryRequest, StoryResponse, Config } from './types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for story generation
});

export const getConfig = async (): Promise<Config> => {
  const response = await api.get('/config');
  return response.data;
};

export const generateStory = async (request: StoryRequest): Promise<StoryResponse> => {
  const response = await api.post('/generate-story', request);
  return response.data;
};

export const getImageUrl = (imagePath: string): string => {
  return `${API_BASE_URL}${imagePath}`;
};

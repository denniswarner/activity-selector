/**
 * API service for communicating with the Activity Selector backend.
 */

import type { Category, Activity, ActivityRequest, ActivityResponse } from '../types/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Mock data for fallback
const mockCategories: Category[] = [
  { name: "Food", description: "Restaurants and dining options", sheet_name: "Food" },
  { name: "Fun", description: "Entertainment and recreational activities", sheet_name: "Fun" },
  { name: "Outdoor", description: "Outdoor activities and adventures", sheet_name: "Outdoor" },
  { name: "Culture", description: "Museums, theaters, and cultural experiences", sheet_name: "Culture" },
];

const mockActivities: Activity[] = [
  { name: "Pizza Place", description: "Great local pizza joint", price_level: "$$", location: "Downtown", category: "Food" },
  { name: "Movie Theater", description: "Latest blockbusters", price_level: "$$", location: "Mall", category: "Fun" },
  { name: "Hiking Trail", description: "Scenic mountain trails", price_level: "Free", location: "State Park", category: "Outdoor" },
  { name: "Art Museum", description: "Contemporary art exhibits", price_level: "$$", location: "Cultural District", category: "Culture" },
];

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  /**
   * Get all available categories.
   */
  async getCategories(): Promise<Category[]> {
    try {
      return await this.request<Category[]>('/api/categories');
    } catch (error) {
      console.warn('Using mock categories due to API failure');
      return mockCategories;
    }
  }

  /**
   * Get activities for a specific category and optional price level.
   */
  async getActivities(
    category: string,
    priceLevel?: string
  ): Promise<Activity[]> {
    try {
      const params = new URLSearchParams({ category });
      if (priceLevel) {
        params.append('price_level', priceLevel);
      }
      
      return await this.request<Activity[]>(`/api/activities?${params.toString()}`);
    } catch (error) {
      console.warn('Using mock activities due to API failure');
      return mockActivities.filter(activity => 
        activity.category === category && 
        (!priceLevel || activity.price_level === priceLevel)
      );
    }
  }

  /**
   * Get random activity suggestions.
   */
  async getSuggestions(request: ActivityRequest): Promise<ActivityResponse> {
    try {
      return await this.request<ActivityResponse>('/api/suggest', {
        method: 'POST',
        body: JSON.stringify(request),
      });
    } catch (error) {
      console.warn('Using mock suggestions due to API failure');
      const filteredActivities = mockActivities.filter(activity => 
        activity.category === request.category && 
        (!request.price_level || activity.price_level === request.price_level)
      );
      
      return {
        activities: filteredActivities.slice(0, request.limit || 5),
        total_found: filteredActivities.length,
        category: request.category,
        price_level: request.price_level
      };
    }
  }

  /**
   * Health check endpoint.
   */
  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    try {
      return await this.request<{ status: string; service: string; version: string }>('/api/health');
    } catch (error) {
      console.warn('Health check failed, returning mock response');
      return { status: 'ok', service: 'mock', version: '1.0.0' };
    }
  }
}

// Export a singleton instance
export const apiService = new ApiService(); 
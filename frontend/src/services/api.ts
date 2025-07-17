/**
 * API service for communicating with the Activity Selector backend.
 */

import type { Category, Activity, ActivityRequest, ActivityResponse } from '../types/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

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
    return this.request<Category[]>('/api/categories');
  }

  /**
   * Get activities for a specific category and optional price level.
   */
  async getActivities(
    category: string,
    priceLevel?: string
  ): Promise<Activity[]> {
    const params = new URLSearchParams({ category });
    if (priceLevel) {
      params.append('price_level', priceLevel);
    }
    
    return this.request<Activity[]>(`/api/activities?${params.toString()}`);
  }

  /**
   * Get random activity suggestions.
   */
  async getSuggestions(request: ActivityRequest): Promise<ActivityResponse> {
    return this.request<ActivityResponse>('/api/suggest', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Health check endpoint.
   */
  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    return this.request<{ status: string; service: string; version: string }>('/api/health');
  }
}

// Export a singleton instance
export const apiService = new ApiService(); 
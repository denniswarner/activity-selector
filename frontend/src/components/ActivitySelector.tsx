/**
 * Main ActivitySelector component that orchestrates the entire application.
 */

import React, { useState, useEffect } from 'react';
import { Header } from './Header';
import { CategoryDropdown } from './CategoryDropdown';
import { PriceSelector } from './PriceSelector';
import { ActivityList } from './ActivityList';
import { apiService } from '../services/api';
import type { Category, Activity, PriceLevelType } from '../types/types';

export const ActivitySelector: React.FC = () => {
  // State management
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedPrice, setSelectedPrice] = useState<PriceLevelType | ''>('');
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [categoriesLoading, setCategoriesLoading] = useState(true);

  // Load categories on component mount
  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setCategoriesLoading(true);
      setError('');
      const categoriesData = await apiService.getCategories();
      setCategories(categoriesData);
    } catch (err) {
      setError('Failed to load categories. Please try again.');
      console.error('Error loading categories:', err);
    } finally {
      setCategoriesLoading(false);
    }
  };

  const getSuggestions = async () => {
    if (!selectedCategory) {
      setError('Please select a category first.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const request = {
        category: selectedCategory,
        price_level: selectedPrice || undefined,
        limit: 6
      };

      const response = await apiService.getSuggestions(request);
      setActivities(response.activities);
    } catch (err) {
      setError('Failed to get suggestions. Please try again.');
      console.error('Error getting suggestions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    setActivities([]); // Clear previous results
    setError('');
  };

  const handlePriceChange = (price: PriceLevelType | '') => {
    setSelectedPrice(price);
    setActivities([]); // Clear previous results
    setError('');
  };

  const handleRetry = () => {
    if (selectedCategory) {
      getSuggestions();
    } else {
      loadCategories();
    }
  };

  const isFormValid = selectedCategory.trim() !== '';

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <Header />
        
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Controls */}
          <div className="lg:col-span-1">
            <div className="card sticky top-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Choose Your Preferences
              </h2>
              
              <div className="space-y-6">
                <CategoryDropdown
                  categories={categories}
                  selectedCategory={selectedCategory}
                  onCategoryChange={handleCategoryChange}
                  loading={categoriesLoading}
                  disabled={loading}
                />
                
                <PriceSelector
                  selectedPrice={selectedPrice}
                  onPriceChange={handlePriceChange}
                  disabled={loading || !selectedCategory}
                />
                
                <button
                  onClick={getSuggestions}
                  disabled={!isFormValid || loading}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Getting Suggestions...
                    </div>
                  ) : (
                    'Get Suggestions'
                  )}
                </button>
              </div>
            </div>
          </div>
          
          {/* Right Column - Results */}
          <div className="lg:col-span-2">
            <ActivityList
              activities={activities}
              loading={loading}
              error={error}
              onRetry={handleRetry}
            />
          </div>
        </div>
      </div>
    </div>
  );
}; 
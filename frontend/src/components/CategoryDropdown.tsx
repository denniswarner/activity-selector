/**
 * Category dropdown component for selecting activity categories.
 */

import React from 'react';
import type { Category } from '../types/types';

interface CategoryDropdownProps {
  categories: Category[];
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
  loading?: boolean;
  disabled?: boolean;
}

export const CategoryDropdown: React.FC<CategoryDropdownProps> = ({
  categories,
  selectedCategory,
  onCategoryChange,
  loading = false,
  disabled = false
}) => {
  return (
    <div className="w-full">
      <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
        Category
      </label>
      <select
        id="category"
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        disabled={disabled || loading}
        className="input-field"
      >
        <option value="">Select a category...</option>
        {categories.map((category) => (
          <option key={category.name} value={category.name}>
            {category.name}
          </option>
        ))}
      </select>
      {loading && (
        <p className="text-sm text-gray-500 mt-1">Loading categories...</p>
      )}
    </div>
  );
}; 
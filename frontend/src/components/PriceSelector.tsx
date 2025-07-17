/**
 * Price selector component with visual price level indicators.
 */

import React from 'react';
import { PriceLevel, type PriceLevelType } from '../types/types';

interface PriceSelectorProps {
  selectedPrice: PriceLevelType | '';
  onPriceChange: (price: PriceLevelType | '') => void;
  disabled?: boolean;
}

export const PriceSelector: React.FC<PriceSelectorProps> = ({
  selectedPrice,
  onPriceChange,
  disabled = false
}) => {
  const priceOptions = [
    { value: '', label: 'Any Price', description: 'All price levels' },
    { value: PriceLevel.FREE, label: 'Free', description: 'No cost activities' },
    { value: PriceLevel.LOW, label: '$', description: 'Low cost activities' },
    { value: PriceLevel.MEDIUM, label: '$$', description: 'Medium cost activities' },
    { value: PriceLevel.HIGH, label: '$$$', description: 'High cost activities' },
    { value: PriceLevel.LUXURY, label: '$$$$', description: 'Luxury activities' },
  ];

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-3">
        Price Level
      </label>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {priceOptions.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => onPriceChange(option.value as PriceLevelType | '')}
            disabled={disabled}
            className={`
              p-4 rounded-lg border-2 transition-all duration-200 text-left
              ${selectedPrice === option.value
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
              }
              ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            <div className="font-semibold text-lg mb-1">
              {option.label}
            </div>
            <div className="text-sm text-gray-600">
              {option.description}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}; 
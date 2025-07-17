/**
 * Activity list component to display suggested activities.
 */

import React from 'react';
import type { Activity } from '../types/types';

interface ActivityListProps {
  activities: Activity[];
  loading?: boolean;
  error?: string;
  onRetry?: () => void;
}

export const ActivityList: React.FC<ActivityListProps> = ({
  activities,
  loading = false,
  error,
  onRetry
}) => {
  if (loading) {
    return (
      <div className="card animate-pulse">
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex items-center space-x-4">
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card text-center">
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <p className="text-lg font-medium">Something went wrong</p>
          <p className="text-gray-600 mt-1">{error}</p>
        </div>
        {onRetry && (
          <button onClick={onRetry} className="btn-primary">
            Try Again
          </button>
        )}
      </div>
    );
  }

  if (activities.length === 0) {
    return (
      <div className="card text-center">
        <div className="text-gray-500">
          <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33" />
          </svg>
          <p className="text-lg font-medium">No activities found</p>
          <p className="text-gray-600 mt-1">Try adjusting your filters</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Suggested Activities ({activities.length})
        </h3>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {activities.map((activity, index) => (
          <div
            key={`${activity.name}-${index}`}
            className="card hover:shadow-xl transition-shadow duration-200 animate-slide-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="flex items-start justify-between mb-3">
              <h4 className="font-semibold text-gray-900 text-lg">
                {activity.name}
              </h4>
              <span className="text-sm font-medium text-gray-600 bg-gray-100 px-2 py-1 rounded">
                {activity.price_level}
              </span>
            </div>
            
            {activity.description && (
              <p className="text-gray-600 mb-3 line-clamp-2">
                {activity.description}
              </p>
            )}
            
            {activity.location && (
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {activity.location}
              </div>
            )}
            
            {activity.address && (
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                {activity.address}
              </div>
            )}
            
            {activity.phone && (
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                {activity.phone}
              </div>
            )}
            
            {activity.url && (
              <div className="mb-2">
                <a 
                  href={activity.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 underline flex items-center"
                >
                  <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Visit Website
                </a>
              </div>
            )}
            
            {activity.past_orders && activity.past_orders.length > 0 && (
              <div className="mb-2">
                <div className="text-sm font-medium text-gray-700 mb-1">Past Orders:</div>
                <div className="text-sm text-gray-600">
                  {activity.past_orders.join(', ')}
                </div>
              </div>
            )}
            
            {activity.last_bill_price && (
              <div className="mb-2">
                <div className="text-sm font-medium text-gray-700">Last Bill:</div>
                <div className="text-sm text-gray-600">
                  ${activity.last_bill_price.toFixed(2)}
                </div>
              </div>
            )}
            
            {activity.last_visit_date && (
              <div className="mb-2">
                <div className="text-sm font-medium text-gray-700">Last Visit:</div>
                <div className="text-sm text-gray-600">
                  {new Date(activity.last_visit_date).toLocaleDateString()}
                </div>
              </div>
            )}
            
            {activity.notes && (
              <div className="mt-3 p-2 bg-blue-50 rounded-lg">
                <div className="text-sm font-medium text-blue-800 mb-1">Notes:</div>
                <div className="text-sm text-blue-700">
                  {activity.notes}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}; 
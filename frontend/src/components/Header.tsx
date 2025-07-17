/**
 * Header component for the Activity Selector app.
 */

import React from 'react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

export const Header: React.FC<HeaderProps> = ({ 
  title = "What do you want to do today?", 
  subtitle = "Let us help you decide on your next adventure!" 
}) => {
  return (
    <header className="text-center mb-8 animate-fade-in">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
        {title}
      </h1>
      <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
        {subtitle}
      </p>
    </header>
  );
}; 
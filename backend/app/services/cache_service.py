"""
Caching service for Google Sheets data to reduce API calls.
"""
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class CacheService:
    """Service for caching Google Sheets data."""
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize the cache service.
        
        Args:
            default_ttl (int): Default time-to-live in seconds (default: 1 hour)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[Any]: Cached value or None if not found/expired
        """
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        if self._is_expired(cache_entry):
            del self._cache[key]
            return None
        
        return cache_entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in cache.
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            ttl (Optional[int]): Time-to-live in seconds (uses default if None)
        """
        ttl = ttl or self._default_ttl
        expiry_time = datetime.now() + timedelta(seconds=ttl)
        
        self._cache[key] = {
            'value': value,
            'expires_at': expiry_time
        }
    
    def delete(self, key: str) -> None:
        """
        Delete a value from cache.
        
        Args:
            key (str): Cache key to delete
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
    
    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """
        Check if a cache entry has expired.
        
        Args:
            cache_entry (Dict[str, Any]): Cache entry to check
            
        Returns:
            bool: True if expired, False otherwise
        """
        return datetime.now() > cache_entry['expires_at']
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        return {
            'total_entries': len(self._cache),
            'default_ttl': self._default_ttl,
            'keys': list(self._cache.keys())
        }


# Global cache instance
cache_service = CacheService() 
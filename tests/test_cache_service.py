"""
Unit tests for the cache service.
"""
import pytest
import time
from datetime import datetime, timedelta
from backend.app.services.cache_service import CacheService


class TestCacheService:
    """Test cases for CacheService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cache = CacheService(default_ttl=60)  # 1 minute TTL for testing
    
    def test_set_and_get(self):
        """Test setting and getting values from cache."""
        # Test basic set and get
        self.cache.set("test_key", "test_value")
        assert self.cache.get("test_key") == "test_value"
        
        # Test with different data types
        self.cache.set("dict_key", {"name": "test", "value": 123})
        assert self.cache.get("dict_key") == {"name": "test", "value": 123}
        
        self.cache.set("list_key", [1, 2, 3, "test"])
        assert self.cache.get("list_key") == [1, 2, 3, "test"]
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        assert self.cache.get("nonexistent_key") is None
    
    def test_custom_ttl(self):
        """Test setting values with custom TTL."""
        # Set with custom TTL (1 second)
        self.cache.set("short_ttl", "value", ttl=1)
        assert self.cache.get("short_ttl") == "value"
        
        # Wait for expiration
        time.sleep(1.1)
        assert self.cache.get("short_ttl") is None
    
    def test_default_ttl(self):
        """Test that default TTL is used when not specified."""
        self.cache.set("default_ttl_key", "value")
        
        # Should still be there immediately
        assert self.cache.get("default_ttl_key") == "value"
        
        # Create a cache with very short default TTL for testing
        short_cache = CacheService(default_ttl=1)
        short_cache.set("test", "value")
        time.sleep(1.1)
        assert short_cache.get("test") is None
    
    def test_delete(self):
        """Test deleting keys from cache."""
        self.cache.set("delete_key", "value")
        assert self.cache.get("delete_key") == "value"
        
        self.cache.delete("delete_key")
        assert self.cache.get("delete_key") is None
        
        # Deleting non-existent key should not raise error
        self.cache.delete("nonexistent_key")
    
    def test_clear(self):
        """Test clearing all cache entries."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        assert self.cache.get("key1") == "value1"
        assert self.cache.get("key2") == "value2"
        assert self.cache.get("key3") == "value3"
        
        self.cache.clear()
        
        assert self.cache.get("key1") is None
        assert self.cache.get("key2") is None
        assert self.cache.get("key3") is None
    
    def test_cache_stats(self):
        """Test getting cache statistics."""
        # Empty cache
        stats = self.cache.get_cache_stats()
        assert stats["total_entries"] == 0
        assert stats["default_ttl"] == 60
        assert stats["keys"] == []
        
        # Add some entries
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        stats = self.cache.get_cache_stats()
        assert stats["total_entries"] == 2
        assert "key1" in stats["keys"]
        assert "key2" in stats["keys"]
    
    def test_expiration_cleanup(self):
        """Test that expired entries are automatically cleaned up."""
        # Set a value with very short TTL
        self.cache.set("expire_key", "value", ttl=1)
        
        # Should be there immediately
        assert self.cache.get("expire_key") == "value"
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be cleaned up and return None
        assert self.cache.get("expire_key") is None
        
        # Check that it's removed from internal cache
        stats = self.cache.get_cache_stats()
        assert "expire_key" not in stats["keys"] 
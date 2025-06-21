import json
import redis.asyncio as redis
from typing import Optional, Any, Dict, List
from datetime import timedelta

from app.core.config import settings

class RedisCache:
    """
    Redis cache manager for the application.
    
    Provides methods for caching user data, contacts, and other frequently
    accessed data with proper security and data freshness.
    """
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def init_cache(self):
        """Initialize Redis connection."""
        self.redis_client = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            password=settings.REDIS_PASSWORD,
            encoding="utf-8",
            decode_responses=True,
        )
    
    async def close_cache(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()
    
    def _get_user_key(self, user_id: int) -> str:
        """Generate cache key for user data."""
        return f"user:{user_id}"
    
    def _get_contacts_key(self, user_id: int) -> str:
        """Generate cache key for user contacts."""
        return f"contacts:{user_id}"
    
    def _get_contact_key(self, contact_id: int, user_id: int) -> str:
        """Generate cache key for specific contact."""
        return f"contact:{contact_id}:user:{user_id}"
    
    async def cache_user(self, user_id: int, user_data: Dict[str, Any], ttl: int = 3600) -> bool:
        """
        Cache user data.
        
        Args:
            user_id: User ID
            user_data: User data to cache
            ttl: Time to live in seconds (default: 1 hour)
            
        Returns:
            bool: True if cached successfully
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_user_key(user_id)
            # Remove sensitive data before caching
            safe_user_data = {
                "id": user_data.get("id"),
                "email": user_data.get("email"),
                "is_active": user_data.get("is_active"),
                "is_verified": user_data.get("is_verified"),
                "role": user_data.get("role"),
            }
            await self.redis_client.setex(
                key, 
                ttl, 
                json.dumps(safe_user_data)
            )
            return True
        except Exception:
            return False
    
    async def get_cached_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get cached user data.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[Dict]: Cached user data or None
        """
        if not self.redis_client:
            return None
        
        try:
            key = self._get_user_key(user_id)
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    async def invalidate_user_cache(self, user_id: int) -> bool:
        """
        Invalidate user cache.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if invalidated successfully
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_user_key(user_id)
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False
    
    async def cache_contacts(self, user_id: int, contacts: List[Dict[str, Any]], ttl: int = 1800) -> bool:
        """
        Cache user contacts list.
        
        Args:
            user_id: User ID
            contacts: List of contacts to cache
            ttl: Time to live in seconds (default: 30 minutes)
            
        Returns:
            bool: True if cached successfully
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_contacts_key(user_id)
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(contacts)
            )
            return True
        except Exception:
            return False
    
    async def get_cached_contacts(self, user_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached contacts list.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[List]: Cached contacts or None
        """
        if not self.redis_client:
            return None
        
        try:
            key = self._get_contacts_key(user_id)
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    async def cache_contact(self, contact_id: int, user_id: int, contact_data: Dict[str, Any], ttl: int = 1800) -> bool:
        """
        Cache specific contact.
        
        Args:
            contact_id: Contact ID
            user_id: User ID
            contact_data: Contact data to cache
            ttl: Time to live in seconds (default: 30 minutes)
            
        Returns:
            bool: True if cached successfully
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_contact_key(contact_id, user_id)
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(contact_data)
            )
            return True
        except Exception:
            return False
    
    async def get_cached_contact(self, contact_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get cached contact.
        
        Args:
            contact_id: Contact ID
            user_id: User ID
            
        Returns:
            Optional[Dict]: Cached contact or None
        """
        if not self.redis_client:
            return None
        
        try:
            key = self._get_contact_key(contact_id, user_id)
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    async def invalidate_contact_cache(self, contact_id: int, user_id: int) -> bool:
        """
        Invalidate specific contact cache.
        
        Args:
            contact_id: Contact ID
            user_id: User ID
            
        Returns:
            bool: True if invalidated successfully
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_contact_key(contact_id, user_id)
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False
    
    async def invalidate_user_contacts_cache(self, user_id: int) -> bool:
        """
        Invalidate all contacts cache for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if invalidated successfully
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_contacts_key(user_id)
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False
    
    async def set_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """
        Set rate limit for a key.
        
        Args:
            key: Rate limit key
            limit: Number of requests allowed
            window: Time window in seconds
            
        Returns:
            bool: True if set successfully
        """
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.setex(key, window, limit)
            return True
        except Exception:
            return False
    
    async def check_rate_limit(self, key: str) -> bool:
        """
        Check if rate limit is exceeded.
        
        Args:
            key: Rate limit key
            
        Returns:
            bool: True if limit not exceeded
        """
        if not self.redis_client:
            return True
        
        try:
            current = await self.redis_client.get(key)
            if current is None:
                return True
            return int(current) > 0
        except Exception:
            return True

# Global cache instance
cache = RedisCache() 
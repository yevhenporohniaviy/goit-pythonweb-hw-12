import pytest
import json
from unittest.mock import AsyncMock, patch
from app.core.cache import RedisCache, cache


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for testing."""
    with patch('app.core.cache.redis.from_url') as mock_redis:
        mock_client = AsyncMock()
        mock_redis.return_value = mock_client
        yield mock_client


@pytest.fixture
async def test_cache(mock_redis_client):
    """Test cache instance."""
    test_cache = RedisCache()
    await test_cache.init_cache()
    return test_cache


class TestRedisCache:
    """Test Redis cache functionality."""
    
    async def test_init_cache(self, mock_redis_client):
        """Test cache initialization."""
        test_cache = RedisCache()
        await test_cache.init_cache()
        
        assert test_cache.redis_client is not None
    
    async def test_cache_user(self, test_cache, mock_redis_client):
        """Test caching user data."""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "is_active": True,
            "is_verified": True,
            "role": "user",
            "hashed_password": "hashed_password"  # Should be filtered out
        }
        
        result = await test_cache.cache_user(1, user_data, ttl=3600)
        
        assert result is True
        mock_redis_client.setex.assert_called_once()
        
        # Check that sensitive data is filtered out
        call_args = mock_redis_client.setex.call_args
        cached_data = json.loads(call_args[0][2])
        assert "hashed_password" not in cached_data
        assert cached_data["email"] == "test@example.com"
    
    async def test_get_cached_user(self, test_cache, mock_redis_client):
        """Test retrieving cached user data."""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "is_active": True,
            "is_verified": True,
            "role": "user"
        }
        mock_redis_client.get.return_value = json.dumps(user_data)
        
        result = await test_cache.get_cached_user(1)
        
        assert result == user_data
        mock_redis_client.get.assert_called_once_with("user:1")
    
    async def test_get_cached_user_not_found(self, test_cache, mock_redis_client):
        """Test retrieving non-existent cached user."""
        mock_redis_client.get.return_value = None
        
        result = await test_cache.get_cached_user(1)
        
        assert result is None
    
    async def test_invalidate_user_cache(self, test_cache, mock_redis_client):
        """Test invalidating user cache."""
        result = await test_cache.invalidate_user_cache(1)
        
        assert result is True
        mock_redis_client.delete.assert_called_once_with("user:1")
    
    async def test_cache_contacts(self, test_cache, mock_redis_client):
        """Test caching contacts list."""
        contacts = [
            {"id": 1, "first_name": "John", "email": "john@example.com"},
            {"id": 2, "first_name": "Jane", "email": "jane@example.com"}
        ]
        
        result = await test_cache.cache_contacts(1, contacts, ttl=1800)
        
        assert result is True
        mock_redis_client.setex.assert_called_once()
        
        call_args = mock_redis_client.setex.call_args
        assert call_args[0][0] == "contacts:1"
        assert call_args[0][1] == 1800
    
    async def test_get_cached_contacts(self, test_cache, mock_redis_client):
        """Test retrieving cached contacts."""
        contacts = [
            {"id": 1, "first_name": "John", "email": "john@example.com"},
            {"id": 2, "first_name": "Jane", "email": "jane@example.com"}
        ]
        mock_redis_client.get.return_value = json.dumps(contacts)
        
        result = await test_cache.get_cached_contacts(1)
        
        assert result == contacts
        mock_redis_client.get.assert_called_once_with("contacts:1")
    
    async def test_cache_contact(self, test_cache, mock_redis_client):
        """Test caching individual contact."""
        contact_data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "user_id": 1
        }
        
        result = await test_cache.cache_contact(1, 1, contact_data, ttl=1800)
        
        assert result is True
        mock_redis_client.setex.assert_called_once()
        
        call_args = mock_redis_client.setex.call_args
        assert call_args[0][0] == "contact:1:user:1"
        assert call_args[0][1] == 1800
    
    async def test_get_cached_contact(self, test_cache, mock_redis_client):
        """Test retrieving cached contact."""
        contact_data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "user_id": 1
        }
        mock_redis_client.get.return_value = json.dumps(contact_data)
        
        result = await test_cache.get_cached_contact(1, 1)
        
        assert result == contact_data
        mock_redis_client.get.assert_called_once_with("contact:1:user:1")
    
    async def test_invalidate_contact_cache(self, test_cache, mock_redis_client):
        """Test invalidating contact cache."""
        result = await test_cache.invalidate_contact_cache(1, 1)
        
        assert result is True
        mock_redis_client.delete.assert_called_once_with("contact:1:user:1")
    
    async def test_invalidate_user_contacts_cache(self, test_cache, mock_redis_client):
        """Test invalidating user contacts cache."""
        result = await test_cache.invalidate_user_contacts_cache(1)
        
        assert result is True
        mock_redis_client.delete.assert_called_once_with("contacts:1")
    
    async def test_cache_redis_connection_error(self, mock_redis_client):
        """Test cache behavior when Redis is not available."""
        test_cache = RedisCache()
        # Don't initialize cache to simulate connection error
        
        result = await test_cache.cache_user(1, {"id": 1, "email": "test@example.com"})
        assert result is False
        
        result = await test_cache.get_cached_user(1)
        assert result is None
    
    async def test_cache_exception_handling(self, test_cache, mock_redis_client):
        """Test cache exception handling."""
        mock_redis_client.setex.side_effect = Exception("Redis error")
        
        result = await test_cache.cache_user(1, {"id": 1, "email": "test@example.com"})
        assert result is False
        
        mock_redis_client.get.side_effect = Exception("Redis error")
        result = await test_cache.get_cached_user(1)
        assert result is None


class TestCacheKeys:
    """Test cache key generation."""
    
    def test_user_key_generation(self):
        """Test user cache key generation."""
        test_cache = RedisCache()
        key = test_cache._get_user_key(123)
        assert key == "user:123"
    
    def test_contacts_key_generation(self):
        """Test contacts cache key generation."""
        test_cache = RedisCache()
        key = test_cache._get_contacts_key(123)
        assert key == "contacts:123"
    
    def test_contact_key_generation(self):
        """Test individual contact cache key generation."""
        test_cache = RedisCache()
        key = test_cache._get_contact_key(456, 123)
        assert key == "contact:456:user:123" 
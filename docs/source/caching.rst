Caching with Redis
=================

The Contacts API uses Redis for caching to improve performance and reduce database load.

## Overview

The caching system provides:

- **User Data Caching**: Frequently accessed user information
- **Contact Caching**: Individual contacts and contact lists
- **Cache Invalidation**: Automatic cache cleanup when data changes
- **Security**: Sensitive data filtering before caching
- **Fallback**: Graceful degradation when Redis is unavailable

## Architecture

### Cache Manager

The `RedisCache` class manages all caching operations:

```python
from app.core.cache import cache

# Cache user data
await cache.cache_user(user_id, user_data, ttl=3600)

# Get cached user
cached_user = await cache.get_cached_user(user_id)

# Invalidate cache
await cache.invalidate_user_cache(user_id)
```

### Cache Keys

Cache keys follow a consistent naming pattern:

- **Users**: `user:{user_id}`
- **Contacts**: `contact:{contact_id}:user:{user_id}`
- **Contact Lists**: `contacts:{user_id}`

## Features

### Security

- **Data Filtering**: Sensitive data (passwords, tokens) is filtered before caching
- **User Isolation**: Cache keys include user ID to prevent data leakage
- **TTL**: Automatic expiration prevents stale data accumulation

### Performance

- **Read-Through Caching**: Data is cached on first read
- **Write-Through Invalidation**: Cache is invalidated on data changes
- **Graceful Degradation**: Application works without cache if Redis is down

### Data Freshness

- **TTL Configuration**: Different TTLs for different data types
- **Cache Invalidation**: Immediate invalidation on data changes
- **Consistency**: Cache is always consistent with database

## Usage Examples

### Caching User Data

```python
# Cache user data (sensitive data filtered automatically)
user_data = {
    "id": 1,
    "email": "user@example.com",
    "is_active": True,
    "is_verified": True,
    "role": "user"
}
await cache.cache_user(1, user_data, ttl=3600)

# Retrieve cached user
cached_user = await cache.get_cached_user(1)
```

### Caching Contacts

```python
# Cache individual contact
contact_data = {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "user_id": 1
}
await cache.cache_contact(1, 1, contact_data, ttl=1800)

# Get cached contact
cached_contact = await cache.get_cached_contact(1, 1)
```

### Cache Invalidation

```python
# Invalidate specific contact cache
await cache.invalidate_contact_cache(contact_id, user_id)

# Invalidate all user contacts
await cache.invalidate_user_contacts_cache(user_id)

# Invalidate user cache
await cache.invalidate_user_cache(user_id)
```

## Configuration

### Redis Settings

Configure Redis in your environment:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

### TTL Settings

Default TTL values:

- **User Data**: 1 hour (3600 seconds)
- **Contacts**: 30 minutes (1800 seconds)
- **Contact Lists**: 30 minutes (1800 seconds)

## Error Handling

The cache system handles errors gracefully:

- **Connection Errors**: Returns `None` or `False` instead of crashing
- **Serialization Errors**: Logs errors and continues without caching
- **Redis Unavailable**: Application continues with database-only operations

## Monitoring

### Cache Hit Rate

Monitor cache effectiveness:

```python
# Check if data is in cache
cached_data = await cache.get_cached_user(user_id)
if cached_data:
    print("Cache hit")
else:
    print("Cache miss")
```

### Cache Health

Check Redis connection:

```python
# Test cache functionality
success = await cache.cache_user(1, {"test": "data"})
if success:
    print("Cache is working")
else:
    print("Cache is not available")
```

## Best Practices

1. **Use Appropriate TTLs**: Set TTLs based on data volatility
2. **Invalidate on Changes**: Always invalidate cache when data changes
3. **Monitor Performance**: Track cache hit rates and adjust TTLs
4. **Handle Failures**: Always have fallback to database
5. **Secure Data**: Never cache sensitive information

## Integration with Services

### Contact Services

Contact services automatically use caching:

```python
# These functions use caching internally
contact = await get_contact_with_cache(db, contact_id, user_id)
contacts = await get_contacts_with_cache(db, user_id, skip, limit)
```

### Authentication Services

User authentication uses caching for performance:

```python
# Cached user retrieval
user = await get_user_by_id_with_cache(db, user_id)
```

## Testing

Cache functionality is thoroughly tested:

```bash
# Run cache tests
pytest tests/unit/test_cache.py

# Run integration tests with cache
pytest tests/integration/
``` 
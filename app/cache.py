import redis.asyncio as redis

from app.settings import settings

client = redis.Redis.from_url(str(settings.REDIS_URL), decode_responses=True)

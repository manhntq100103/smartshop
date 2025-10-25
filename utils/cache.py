import redis
import json

CACHE_TTL = 600

redis_client = redis.Redis(host="localhost", port="6379")

def set_to_cache(cache_key, data):
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))

def get_from_cache(cache_key):
    cache_data = redis_client.get(cache_key)
    if not cache_data:
        return None
    
    return json.loads(cache_data)
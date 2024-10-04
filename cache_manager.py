import aioredis

class CacheManager:
    def __init__(self):
        self.redis = aioredis.from_url("redis://localhost")

    async def cache_product(self, product: dict):
        key = f"product:{product['product_title']}"
        await self.redis.set(key, product['product_price'])

    async def is_product_cached(self, product: dict) -> bool:
        key = f"product:{product['product_title']}"
        cached_price = await self.redis.get(key)
        return cached_price == product['product_price']


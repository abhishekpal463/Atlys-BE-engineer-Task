import aioredis

class CacheManager:
    def __init__(self):
        self.redis = aioredis.from_url("redis://localhost")

    async def cache_product(self, product: dict):
        key = product['product_title']
        await self.redis.set(key, product['product_price'])

    async def is_product_cached(self, product: dict) -> bool:
        key = product['product_title']
        cached_price = await self.redis.get(key)
        if cached_price is not None:
            cached_price = cached_price.decode('utf-8')
            cached_price = float(cached_price)
            return cached_price == product['product_price']
        return False


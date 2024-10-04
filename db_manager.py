import json
import os
from typing import List
import logging

from cache_manager import CacheManager


class DBManager:
    def __init__(self, file_path: str = "products.json", cache: CacheManager = None):
        self.file_path = file_path
        self.cache = cache if cache else CacheManager()

    def save(self, products: List[dict]):
        # Ensure only serializable objects are passed to json.dump
        with open(self.file_path, "w") as f:
            json.dump(products, f, indent=4)

    def load(self) -> List[dict]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    async def update_products(self, new_products: List[dict]) -> int:
        old_products = self.load()
        updated = 0

        for product in new_products:
            # Ensure proper awaiting of async cache check
            cached = await self.cache.is_product_cached(product)  # Make sure to await async functions
            if cached:
                continue  # Skip updating if the product price hasn't changed

            # Otherwise, cache the product and update the DB
            if product['product_price'] is not None:
                await self.cache.cache_product(product)  # Await this as well to avoid coroutine issues
            old_products.append(product)
            updated += 1

        # Save updated products to the JSON file
        self.save(old_products)

        return updated

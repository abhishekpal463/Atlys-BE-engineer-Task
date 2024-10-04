import json
import os
from typing import List


class DBManager:
    def __init__(self, file_path: str = "products.json"):
        self.file_path = file_path

    def save(self, products: List[dict]):
        with open(self.file_path, "w") as f:
            json.dump(products, f, indent=4)

    def load(self) -> List[dict]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    def update_products(self, new_products: List[dict]) -> int:
        old_products = self.load()
        updated = 0
        for product in new_products:
            # Update logic if product has changed
            old_product = next((p for p in old_products if p['product_title'] == product['product_title']), None)
            if old_product and old_product['product_price'] == product['product_price']:
                continue  # Skip if the price hasn't changed
            old_products.append(product)
            updated += 1

        self.save(old_products)
        return updated

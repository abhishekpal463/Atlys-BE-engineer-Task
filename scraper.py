import aiohttp
from bs4 import BeautifulSoup
import os
from typing import List, Optional
import asyncio

from cache_manager import CacheManager


class Scraper:
    def __init__(self, base_url: str, max_pages: Optional[int] = None, proxy: Optional[str] = None):
        self.base_url = base_url
        self.max_pages = max_pages
        self.proxy = proxy
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    async def fetch_page(self, session, url: str) -> str:
        retries = 3
        while retries > 0:
            try:
                async with session.get(url, proxy=self.proxy, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        retries -= 1
                        await asyncio.sleep(2)  # Retry delay
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                retries -= 1
        return ""

    async def scrape_product_info(self, html: str) -> List[dict]:
        soup = BeautifulSoup(html, 'lxml')
        products = []
        for product in soup.find_all('div', class_='mf-product-details'):
            title = product.find('h2', class_='woo-loop-product__title').text.strip()
            # Extract price using the specific span
            price = product.find('span', class_='woocommerce-Price-amount amount')
            price_amount = ''

            if price:
                price_bdi = price.find('bdi').text.strip() if price.find('bdi') else None
                if price_bdi:
                    # Remove the currency symbol and commas, and strip whitespace
                    price_amount = price_bdi.replace('₹', '').replace(',', '').strip()

                    # Convert the cleaned price string to a float
                    try:
                        price_amount = float(price_amount)
                    except ValueError:
                        price_amount = 0.0  # Default to 0.0 if conversion fails

            # Handle case where price is not found or cannot be converted
            if not price_amount:
                price_amount = 0.0

            thumbnail_div = product.find_previous('div', class_='mf-product-thumbnail')  # Adjust this if necessary
            img = thumbnail_div.find('img') if thumbnail_div else None

            # Try to fetch the correct image URL
            if img:
                # Check the src attribute for the image URL
                img_url = img.get('data-lazy-src') or img.get('src')  # Prefer lazy load URL
            else:
                img_url = None  # Fallback if no image is found

            # Download and save image locally if img_url exists
            img_path = await self.download_image(img_url) if img_url else None

            products.append({
                "product_title": title,
                "product_price": price_amount,
                "path_to_image": img_path
            })
        return products

    async def download_image(self, img_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as resp:
                img_name = img_url.split("/")[-1]
                img_path = f"images/{img_name}"
                with open(img_path, 'wb') as img_file:
                    img_file.write(await resp.read())
        return img_path

    async def scrape(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page_num in range(1, self.max_pages + 1):
                if page_num==1:
                    url = f"{self.base_url}/"
                else:
                    url = f"{self.base_url}/page/{page_num}/"
                tasks.append(self.fetch_page(session, url))

            pages_content = await asyncio.gather(*tasks)
            products = []
            for page in pages_content:
                if page:
                    products.extend(await self.scrape_product_info(page))
            return products

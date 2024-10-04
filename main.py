from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional

from cache_manager import CacheManager
from db_manager import DBManager
from notifier import Notifier
from scraper import Scraper

app = FastAPI()

API_TOKEN = "secret_token"


def authenticate(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/scrape")
async def scrape(token: str = Depends(authenticate), page: int = 5, proxy: Optional[str] = None):
    scraper = Scraper(base_url="https://dentalstall.com/shop/", max_pages=page, proxy=proxy)
    products = await scraper.scrape()
    cache_manager = CacheManager()
    db_manager = DBManager(cache=cache_manager)
    updated_count = await db_manager.update_products(products)

    Notifier.notify(len(products))
    return {"scraped_products": len(products), "updated_products": updated_count}
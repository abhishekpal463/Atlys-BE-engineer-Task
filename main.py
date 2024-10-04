from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional

from db_manager import DBManager
from notifier import Notifier
from scraper import Scraper

app = FastAPI()

API_TOKEN = "secret_token"


def authenticate(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/scrape")
async def scrape(token: str = Depends(authenticate), max_pages: int = 5, proxy: Optional[str] = None):
    scraper = Scraper(base_url="https://dentalstall.com/shop/", max_pages=max_pages, proxy=proxy)
    products = await scraper.scrape()
    print(products)
    db_manager = DBManager()
    updated_count = db_manager.update_products(products)

    Notifier.notify(len(products))
    return {"scraped_products": len(products), "updated_products": updated_count}
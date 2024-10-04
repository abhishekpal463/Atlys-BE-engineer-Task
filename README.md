**Python Web Scraping with FastAPI**

> Environment setup 
```
> Clone the repository and navigate to the project directory.
> Install dependencies via pip install -r requirements.txt
> Run FastAPI server: uvicorn main:app --reload
```
> API Endpoint

`Curl to start the scraping`

``curl --location 'localhost:8000/scrape?token=secret_token&max_pages=1' \
--header 'Content-Type: application/json'``
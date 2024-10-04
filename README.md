**Python Web Scraping with FastAPI**

> Environment setup 
```
> Clone the repository and navigate to the project directory.
> Install dependencies via pip install -r requirements.txt
> Install redis
> Start redis server via redis-server
> Run FastAPI server: uvicorn main:app --reload
```
> API Endpoint

`Curl to start the scraping`

``curl --location 'localhost:8000/scrape?token=PROVIDE_TOKEN&page=1' \
--header 'Content-Type: application/json'``
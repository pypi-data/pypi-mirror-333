from fastapi import FastAPI
from crawler import IntelligentWebCrawler

app = FastAPI()


@app.get("/scrape")
def scrape_website(url: str):
    crawler = IntelligentWebCrawler(url)
    json = crawler.fetch(url)
    return json
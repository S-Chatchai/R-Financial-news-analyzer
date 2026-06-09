import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
from pymongo import MongoClient, UpdateOne

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import LLMExtractionStrategy, LLMConfig

# --- Configuration ---
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI") 
OUTPUT_FILE = "infoquest_news_test.json"

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Please check your .env file.")
if not MONGODB_URI:
    raise ValueError("❌ MONGODB_URI not found. Please check your .env file.")

class Article(BaseModel):
    title: Optional[str] = Field(description="The article headline (in original language)")
    link: Optional[str] = Field(description="The full URL or relative path to the article")
    # time: Optional[str] = Field(description="The published time or date (as shown on the page)")

async def main():
    target_urls = [
        "https://www.infoquest.co.th/stock",
        "https://www.posttoday.com/business/stockholder",
        "https://www.thansettakij.com/category/finance/stockmarket",
        "https://www.kaohoon.com/"
    ]

    print(f"[{datetime.now().strftime('%H:%M:%S')}] ☁️ Connecting to MongoDB Atlas...")
    client = MongoClient(MONGODB_URI)
    db = client["finance_db"] 
    collection = db["news_articles"] 

    llm_config = LLMConfig(
        provider="gemini/gemini-2.5-flash-lite", 
        api_token=GEMINI_API_KEY
    )
    
    extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        schema=Article.model_json_schema(), 
        extraction_type="schema",
        instruction=(
            "Extract ALL news articles you can find from the scraped Thai financial news website content. "
            "Return an array of objects matching the provided schema. If a field is not found, leave it null."
        )
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS 
    )

    async with AsyncWebCrawler() as crawler:
        for target_url in target_urls:
            print(f"\n{'-'*50}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Starting crawler on: {target_url}")

            result = await crawler.arun(
                url=target_url,
                config=crawl_config
            )

            if not result.success:
                print(f"❌ Crawl failed for {target_url}:", result.error_message)
                continue # Skip to the next URL if this one fails

            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Extraction successful. Parsing data...")
            
            try:
                extracted_data = json.loads(result.extracted_content)
            except (json.JSONDecodeError, TypeError):
                print(f"❌ Failed to parse extracted content for {target_url}.")
                continue

            if isinstance(extracted_data, dict):
                articles = next((v for v in extracted_data.values() if isinstance(v, list)), [extracted_data])
            else:
                articles = extracted_data

            if not articles:
                print(f"⚠️ No articles found for {target_url}.")
                continue

            # --- Database Update ---
            operations = []
            for article in articles:
                if article.get("link"):
                    article["scraped_at"] = datetime.now().isoformat()
                    article["source"] = target_url
                    
                    operations.append(
                        UpdateOne(
                            {"link": article["link"]}, 
                            {"$set": article},         
                            upsert=True
                        )
                    )

            if operations:
                db_result = collection.bulk_write(operations)
                print(f"✅ MongoDB Update for {target_url}: {db_result.upserted_count} inserted, {db_result.modified_count} updated.")

            print(f"Preview (Top 1 from {target_url}):")
            print(json.dumps(articles[:1], ensure_ascii=False, indent=2))
            
    print(f"\n{'-'*50}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 All scraping tasks completed.")

if __name__ == "__main__":
    asyncio.run(main())
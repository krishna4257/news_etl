import pandas as pd
import extract
def transform_news(news_data):
    news_list = []
    for article in news_data:
        news_list.append({
            "source": article["source"]["name"],
            "author": article.get("author", "Unknown"),
            "title": article["title"],
            "description": article.get("description", "No description"),
            "url": article["url"],
            "published_at": article["publishedAt"]
        })
    return pd.DataFrame(news_list)

# Transform data
news_df = transform_news(extract.news_data)
print(news_df.head())

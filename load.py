from sqlalchemy import create_engine
import pandas as pd
import requests
import extract
import transform

# Your Neon Database Connection URL
NEON_DB_URL = "postgresql://neondb_owner:npg_MK6o1dlcgmAu@ep-lingering-feather-a5hcyr4n-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"


def load_news_to_neon(news_df):
    """Load transformed news data into Neon PostgreSQL."""
    try:
        engine = create_engine(NEON_DB_URL)
        news_df.to_sql("news_articles", engine, if_exists="append", index=False)
        print("Data successfully loaded into Neon DB!")
    except Exception as e:
        print(f"Error loading data: {e}")

# Run ETL
news_data = extract.extract_news()
news_df = transform.transform_news(news_data)
load_news_to_neon(news_df)

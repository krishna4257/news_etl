from sqlalchemy import create_engine
import pandas as pd
import requests
import extract
import transform

# Your Neon Database Connection URL
NEON_DB_URL = "postgresql://neondb_owner:npg_MK6o1dlcgmAu@ep-lingering-feather-a5hcyr4n-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

def load_news_to_neon(news_data):
    """Load transformed news data into NeonDB (PostgreSQL) using SQLAlchemy."""
    
    # ✅ Convert `news_data` (list of dicts) into a Pandas DataFrame
    df = pd.DataFrame(news_data)
    
    # ✅ If DataFrame is empty, log a warning and exit
    if df.empty:
        print("⚠️ No data to load into NeonDB.")
        return
    
    try:
        # ✅ Establish a database connection
        engine = create_engine(NEON_DB_URL)

        # ✅ Use `.begin()` for transactional integrity
        with engine.begin() as conn:
            df.to_sql("news_articles", conn, if_exists="append", index=False, method="multi")
        
        print(f"✅ Successfully loaded {len(df)} articles into NeonDB!")

    except Exception as e:
        print(f"❌ Error loading data: {e}")


import time
import json
from extract import extract_news
from transform import transform_news
from load import load_news_to_neon

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    print("Starting ETL process...")
    news_data = extract_news()
    news_df = transform_news(news_data)
    load_news_to_neon(news_df)
    print("ETL process completed!")
    return {
        'statusCode': 200,
        'body': json.dumps('News ETL Pipeline Completed Successfully!')
    }
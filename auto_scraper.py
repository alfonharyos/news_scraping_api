import pandas as pd
from base_news_scraper import scrape_news

def update_news():
    pd.concat([
        scrape_news(
            max_page=1
            ),
        pd.read_csv(
            'stunting_data/news_stunting.csv', 
            delimiter=';'
            )
    ]).drop_duplicates()\
        .sort_values(by='tgl',ascending=False)\
            .reset_index(drop=True)\
                .to_csv('stunting_data/news_stunting.csv', sep=';', encoding='utf-8', index=False)
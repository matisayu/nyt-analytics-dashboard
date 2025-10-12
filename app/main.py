from app.db import init_db, engine, get_session
from app.nyt_client import fetch_most_popular, store_stories
from sqlmodel import Session
from analytics.trends import aggregate_popular_stats

def main():
    init_db()
    window_map = {      
        "1d": 1,
        "7d": 7,
        "30d": 30
    }
    with Session(engine) as session:
        for window_label, api_value in window_map.items():            
            stories_data = fetch_most_popular(api_window=api_value)
            store_stories(session, stories_data, api_window=window_label)
        aggregate_popular_stats(session)

if __name__ == "__main__":
    main()
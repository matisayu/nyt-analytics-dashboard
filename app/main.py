from app.db import init_db, session_context
from app.nyt_client import fetch_most_popular, store_stories

def run_daily_story_collection():
    init_db() 

    window_map = {
        "1d": 1,
        "7d": 7,
        "30d": 30
    }

    with session_context() as session:
        for window_label, api_value in window_map.items():
            print(f"Fetching {window_label} popular stories...")
            stories_data = fetch_most_popular(api_window=api_value)
            store_stories(session, stories_data, api_window=window_label)

    print("Story collection complete.")

if __name__ == "__main__":
    run_daily_story_collection()

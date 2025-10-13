import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from sqlmodel import Session, select
from app.models import PopStory
import json

# Map API windows to NYT parameter values
WINDOW_MAP = {"1d": 1, "7d": 7, "30d": 30}

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_most_popular(api_window: str) -> list[dict]:
    url = f"https://api.nytimes.com/svc/mostpopular/v2/viewed/{api_window}.json?api-key={API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["results"]

def store_stories(session: Session, stories_data: list[dict], api_window: str):
    new_count = 0
    updated_count = 0

    for item in stories_data:
        title = item.get("title")
        if not title:
            continue  

        # Check if story already exists (by title)
        existing_story = session.exec(
            select(PopStory).where(PopStory.title == title)
        ).first()

        if existing_story:
            # Update popularity windows if this window is not already included
            windows = json.loads(existing_story.popularity_windows or "[]")
            if api_window not in windows:
                windows.append(api_window)
                existing_story.popularity_windows = json.dumps(windows)
                updated_count += 1
            continue  # skip creating a new record

        # Create a new PopStory entry
        story = PopStory(
            title=title,
            published_date=item.get("published_date"),
            url = item.get("url"),
            section = item.get("section"),
            date_collected=datetime.now().strftime("%Y-%m-%d"),
            popularity_windows=json.dumps([api_window])
        )
        story.set_facets(item.get("geo_facet", []), item.get("des_facet", []), item.get("org_facet", []))

        session.add(story)
        new_count += 1

    session.commit()
    print(
        f"Stored {new_count} new stories, updated {updated_count} existing stories "
        f"(skipped {len(stories_data) - new_count - updated_count} duplicates)"
    )

def fetch_and_store_all_windows(session: Session):
    """Fetch & store stories for all time windows."""
    for key, value in WINDOW_MAP.items():
        print(f"\nFetching {value} stories...")
        stories_data = fetch_most_popular(api_window=value)
        store_stories(session, stories_data, api_window=key)
        
        
        
        
#arts, automobiles, books/review, business, fashion, food, health, home, insider, magazine,
# movies, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, t-magazine, travel, upshot, us, world
#section = "nyregion"
#top_stories_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json"
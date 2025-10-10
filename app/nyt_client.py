import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from sqlmodel import Session, select
from app.models import PopStory
import json

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_most_popular() -> list[dict]:
    url = f"https://api.nytimes.com/svc/mostpopular/v2/viewed/7.json?api-key={API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["results"]

def store_stories(session: Session, stories_data: list[dict]):
    new_count = 0

    for item in stories_data:
        title = item.get("title")
        if not title:
            continue  # skip malformed data

        # Check if story already exists (by title)
        existing_story = session.exec(
            select(PopStory).where(PopStory.title == title)
        ).first()

        if existing_story:
            continue  # skip duplicate

        # Create a new PopStory entry
        story = PopStory(
            title=title,
            published_date=item.get("published_date"),
            date_collected=datetime.now().strftime("%Y-%m-%d"),
        )
        story.set_facets(item.get("geo_facet", []), item.get("des_facet", []))

        session.add(story)
        new_count += 1

    session.commit()
    print(f"Stored {new_count} new stories (skipped {len(stories_data) - new_count} duplicates)")




#arts, automobiles, books/review, business, fashion, food, health, home, insider, magazine,
# movies, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, t-magazine, travel, upshot, us, world
#section = "nyregion"
#top_stories_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json"
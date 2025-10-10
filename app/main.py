from app.db import init_db, engine, get_session
from app.nyt_client import fetch_most_popular, store_stories
from sqlmodel import Session

def main():
    init_db()
    with Session(engine) as session:
        stories = fetch_most_popular()
        store_stories(session, stories)

if __name__ == "__main__":
    main()
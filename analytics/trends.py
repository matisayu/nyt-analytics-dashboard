from sqlmodel import Session, select
import json
from collections import Counter
from datetime import datetime
from app.models import PopStory
from app import utils

MIN_KEYWORD_COUNT = 2

def get_top_sections(session: Session, limit=10):
    results = session.exec(select(PopStory.section))
    counts = Counter(results)
    return counts.most_common(limit)

def get_top_keywords(session: Session, limit=10):
    results = session.exec(select(PopStory.des_facet))
    all_keywords = []
    for r in results:
        if r:
            all_keywords.extend(json.loads(r))
    counts = Counter(all_keywords)
    return counts.most_common(limit)

def aggregate_popular_stats(session: Session):
    """
    Aggregates data from PopStory into SectionStat and KeywordStat tables.
    Groups by api_window and computes counts per section and per keyword.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    # Get all stories
    stories = session.exec(select(PopStory)).all()
    if not stories:
        print("No stories found to aggregate.")
        return

    # Organize by window (each story can appear in multiple)
    window_section_counts = {}
    window_keyword_counts = {}

    for story in stories:
        windows = json.loads(story.popularity_windows or "[]")
        for api_window in windows:
            # Init counters if needed
            window_section_counts.setdefault(api_window, Counter())
            window_keyword_counts.setdefault(api_window, Counter())

            # Increment section count
            if story.section:
                window_section_counts[api_window][story.section] += 1

            # Increment keywords (des_facet)
            try:
                desc_facets = json.loads(story.desc_facet or "[]")
            except json.JSONDecodeError:
                desc_facets = []

            for kw in desc_facets:
                window_keyword_counts[api_window][kw] += 1


    # Write aggregated data using upsert helpers
    for api_window, section_counts in window_section_counts.items():
        for section, count in section_counts.items():
            utils.upsert_section_stat(session, section, count, int(api_window.replace("d", "")), today)

    for api_window, keyword_counts in window_keyword_counts.items():
        for kw, count in keyword_counts.items():
            if count >= MIN_KEYWORD_COUNT:
                utils.upsert_keyword_stat(session, kw, count, int(api_window.replace("d", "")), today)


    session.commit()
    print(f"Aggregated stats for {today}: sections={len(window_section_counts)}, keywords={len(window_keyword_counts)}")

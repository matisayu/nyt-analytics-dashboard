from sqlmodel import Session, select
from app.models import SectionStat, KeywordStat

def upsert_section_stat(session: Session, section: str, story_count: int, api_window: int, date_collected: str):
    existing = session.exec(
        select(SectionStat)
        .where(
            SectionStat.section == section,
            SectionStat.api_window == api_window,
            SectionStat.date_collected == date_collected,
        )
    ).first()

    if existing:
        existing.story_count = story_count  # update existing
    else:
        new_stat = SectionStat(
            section=section,
            story_count=story_count,
            api_window=api_window,
            date_collected=date_collected,
        )
        session.add(new_stat)


def upsert_keyword_stat(session: Session, keyword: str, keyword_count: int, api_window: int, date_collected: str):
    existing = session.exec(
        select(KeywordStat)
        .where(
            KeywordStat.keyword == keyword,
            KeywordStat.api_window == api_window,
            KeywordStat.date_collected == date_collected,
        )
    ).first()

    if existing:
        existing.keyword_count = keyword_count  # update existing
    else:
        new_stat = KeywordStat(
            keyword=keyword,
            keyword_count=keyword_count,
            api_window=api_window,
            date_collected=date_collected,
        )
        session.add(new_stat)

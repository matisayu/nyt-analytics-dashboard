from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timedelta
from app.db import get_session
from app.models import SectionStat

router = APIRouter(prefix="/sections", tags=["Sections"])

# Return top 10 sections for a given window (1, 7, 30)
@router.get("/{window}")
def get_top_sections(window: int, session: Session = Depends(get_session)):
    #Return top 10 sections for a given window (1, 7, or 30 days)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if window not in [1, 7, 30]:
        raise HTTPException(status_code=400, detail="Invalid window. Use 1, 7, or 30.")

    query = (
    select(SectionStat.section, SectionStat.story_count)
    .where(
        SectionStat.api_window == window,
        SectionStat.date_collected == yesterday
    )
    .order_by(SectionStat.story_count.desc())
    .limit(10)
    )
    results = session.exec(query).all()
    return [{"section": r[0], "story_count": r[1]} for r in results]

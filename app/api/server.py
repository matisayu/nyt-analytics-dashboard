from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, session_context
from app.models import SectionStat, KeywordStat, PopStory
from app.api.routes import sections

app = FastAPI(title="NYT Analytics API")


origins = [
    "http://localhost:5173", #dev
    "", #prod
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sections.router)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def root():
    return {"message": "NYT Analytics API is running"}

# GET /sections/?api_window=1
@app.get("/sections/")
def get_sections(api_window: int = 7, session: Session = Depends(get_session)):
    results = session.exec(
        select(SectionStat)
        .where(SectionStat.api_window == api_window)
        .order_by(SectionStat.story_count.desc())
        .limit(10)
    ).all()
    return results

# GET /keywords/?api_window=1
@app.get("/keywords/")
def get_keywords(api_window: int = 7, session: Session = Depends(get_session)):
    results = session.exec(
        select(KeywordStat)
        .where(KeywordStat.api_window == api_window)
        .order_by(KeywordStat.keyword_count.desc())
        .limit(10)
    ).all()
    return results

#GET /stories/?api_window=7d
@app.get("/stories/")
def get_popular_stories(api_window: str = "7d", session: Session = Depends(get_session)):
    results = session.exec(
        select(PopStory)
        .where(PopStory.popularity_windows.contains(api_window))
        .limit(20)
    ).all()
    return results

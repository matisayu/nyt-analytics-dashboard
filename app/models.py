from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint
from typing import Optional, List
from datetime import datetime
import json

class PopStory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, unique=True)
    section: str
    geo_facet: Optional[str] = None
    desc_facet: Optional[str] = None
    org_facet: Optional[str] = None
    url: str
    published_date: str
    date_collected: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))  
    popularity_windows: str = Field(default="[]")

    def set_facets(self, geo_list: List[str], desc_list: List[str], org_list: List[str]):
        self.geo_facet = json.dumps(geo_list)
        self.desc_facet = json.dumps(desc_list)
        self.org_facet = json.dumps(org_list)

    def get_facets(self):
        return {
            "geo_facet": json.loads(self.geo_facet or "[]"),
            "desc_facet": json.loads(self.desc_facet or "[]"),
            "org_facet": json.loads(self.org_facet or "[]")
        }
        

class SectionStat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    section: str
    story_count: int
    date_collected: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    api_window: int

    __table_args__ = (
        UniqueConstraint("section", "api_window", "date_collected", name="uix_section_window_date"),
    )


class KeywordStat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str
    keyword_count: int
    date_collected: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    api_window: int

    __table_args__ = (
        UniqueConstraint("keyword", "api_window", "date_collected", name="uix_keyword_window_date"),
    )
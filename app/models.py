from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import json

class PopStory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, unique=True)
    published_date: str
    geo_facet: Optional[str] = None
    desc_facet: Optional[str] = None
    date_collected: str = datetime.now().strftime("%Y-%m-%d")
    popularity_windows: str = Field(default="[]")

    def set_facets(self, geo_list: List[str], desc_list: List[str]):
        self.geo_facet = json.dumps(geo_list)
        self.desc_facet = json.dumps(desc_list)

    def get_facets(self):
        return {
            "geo_facet": json.loads(self.geo_facet or "[]"),
            "desc_facet": json.loads(self.desc_facet or "[]")
        }

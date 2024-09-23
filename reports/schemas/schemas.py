from datetime import datetime
from typing import List
from pydantic import BaseModel
from typing import Optional


class ReportBaseSchema(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    image_url: Optional[str] = None
    infered_image_url: Optional[str] = None
    lon: float
    lat:float
    categories: List[str]  = []
    createdAt:  Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListReportsResponse(BaseModel):
    status: str
    results: int
    reports: List[ReportBaseSchema]
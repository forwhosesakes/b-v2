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
    pollution_parameter : Optional[float]
    severity:Optional[str] = None
    status : Optional[str] = None
    villa: Optional[float]
    villa_style_loc :Optional[str] = None
    neighbor: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListReportsResponse(BaseModel):
    status: str
    results: int
    totalRecords:int
    reports: List[ReportBaseSchema]
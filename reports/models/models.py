from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Double, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from utils.db import Base

# Association table for the many-to-many relationship
report_categories = Table('report_categories', Base.metadata,
    Column('report_id', Integer, ForeignKey('reports.id')),
    Column('category_id', GUID, ForeignKey('categories.id'))
)

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    lon = Column(Double, nullable=True)
    lat = Column(Double, nullable=True)
    image_url = Column(String, nullable=True)
    pollution_parameter = Column(Double, nullable=True)
    infered_image_url = Column(String, nullable=True)
    severity= Column(String, nullable=True)
    status = Column(String, nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
    villa= Column(String, nullable=True)
    villa_style_loc = Column(String, nullable=True)
    #Relationship to neighbor
    neighbor_id= Column(GUID, ForeignKey('neighbors.id'))
    
    # Relationship to categories
    categories = relationship("Category", secondary=report_categories, back_populates="reports")

class Category(Base):
    __tablename__ = "categories"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable=False, unique=True)
    
    # Relationship to reports
    reports = relationship("Report", secondary=report_categories, back_populates="categories")
    
 
class Neighbor(Base): 
    __tablename__="neighbors"
    id= Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name= Column(String, nullable=False, unique=True)
    reports = relationship("Report",  backref="reports")
     
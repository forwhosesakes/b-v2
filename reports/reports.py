from sqlalchemy.orm import Session, joinedload, join
from fastapi import Depends, HTTPException, status, APIRouter, Response
from utils.db import get_db
from reports.schemas.schemas import ReportBaseSchema  
from reports.models.models import Report, Category
router = APIRouter()


@router.get('/report')
def get_reports(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    print("db")
    print(db)
    skip = (page - 1) * limit
    reports = (db.query(Report)
               .options(joinedload(Report.categories))
               .filter(Report.title.contains(search))
               .order_by(Report.createdAt.desc())
               .limit(limit)
               .offset(skip)
               .all())
    return {'status': 'success', 'results': len(reports), 'reports': reports}


@router.post('/report', status_code=status.HTTP_201_CREATED)
def create_report(payload: ReportBaseSchema, db: Session = Depends(get_db)):
    #Get categories into proper format 
    catesgories_db = db.query(Category).filter(Category.name.in_(payload.categories)).all()
    dic = payload.dict().copy()
    dic['categories']=catesgories_db
    new_report = Report(**dic)
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return {"status": "success", "report": new_report}


@router.patch('/report/{reportId}')
def update_report(reportId: str, payload: ReportBaseSchema, db: Session = Depends(get_db)):
    # Query the report once
    db_report = db.query(Report).filter(Report.id == reportId).first()
    
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No report with id: {reportId} found'
        )
    categories_db = db.query(Category).filter(Category.name.in_(payload.categories)).all()
    # Update the report attributes
    update_data = payload.dict(exclude={'categories'})
    for key, value in update_data.items():
        setattr(db_report, key, value)
    
    # Update categories
    db_report.categories = categories_db
    
    # Commit changes
    db.commit()
    db.refresh(db_report)
    
    return {"status": "success", "report": db_report}


@router.get('/report/{reportId}')
def get_report(reportId: str, db: Session = Depends(get_db)):
    report = db.query(Report).options(joinedload(Report.categories)).filter(Report.id == reportId).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No report with this id: {id} found")
    return {"status": "success", "report": report}


@router.delete('/report/{reportId}')
def delete_report(reportId: str, db: Session = Depends(get_db)):
    report_query = db.query(Report).filter(Report.id == reportId)
    report = report_query.first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No report with this id: {id} found')
    report_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
from fastapi import FastAPI, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import init_db, get_db, IssueDB, Status, Priority

# Initialize the database
init_db()

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IssueBase(BaseModel):
    title: str
    status: Status
    priority: Priority
    assignee: Optional[str] = None

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    assignee: Optional[str] = None

class Issue(IssueBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Helper function to convert DB model to Pydantic model
def issue_from_db(issue_db: IssueDB) -> Issue:
    return Issue.model_validate(issue_db)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/issues", response_model=Issue, status_code=status.HTTP_201_CREATED)
def create_issue(issue_data: IssueCreate, db: Session = Depends(get_db)):
    db_issue = IssueDB(
        id=str(uuid.uuid4()),
        title=issue_data.title,
        status=issue_data.status,
        priority=issue_data.priority,
        assignee=issue_data.assignee
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return issue_from_db(db_issue)

@app.get("/issues", response_model=List[Issue])
def get_issues(
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    sortBy: str = "updatedAt",
    order: str = "desc",
    page: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db)
):
    # Map frontend field names to database column names
    field_mapping = {
        "updatedAt": "updated_at",
        "createdAt": "created_at",
    }

    # Convert sortBy to database column name
    sort_column = field_mapping.get(sortBy, sortBy.lower())

    query = db.query(IssueDB)

    if search:
        query = query.filter(IssueDB.title.ilike(f"%{search}%"))
    if status:
        query = query.filter(IssueDB.status == status)
    if priority:
        query = query.filter(IssueDB.priority == priority)
    if assignee:
        query = query.filter(IssueDB.assignee.ilike(f"%{assignee}%"))

    # Handle sorting
    if hasattr(IssueDB, sort_column):
        column = getattr(IssueDB, sort_column)
        query = query.order_by(column.desc() if order.lower() == "desc" else column.asc())

    # Pagination
    offset = (page - 1) * pageSize
    issues = query.offset(offset).limit(pageSize).all()

    return [issue_from_db(issue) for issue in issues]

@app.get("/issues/{issue_id}", response_model=Issue)
def get_issue(issue_id: str, db: Session = Depends(get_db)):
    db_issue = db.query(IssueDB).filter(IssueDB.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue_from_db(db_issue)

@app.put("/issues/{issue_id}", response_model=Issue)
def update_issue(
    issue_id: str,
    issue_update: IssueUpdate,
    db: Session = Depends(get_db)
):
    db_issue = db.query(IssueDB).filter(IssueDB.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")

    update_data = issue_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_issue, key, value)

    db_issue.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_issue)
    return issue_from_db(db_issue)

@app.delete("/issues/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str, db: Session = Depends(get_db)):
    db_issue = db.query(IssueDB).filter(IssueDB.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")

    db.delete(db_issue)
    db.commit()
    return None
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./issuetracker.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Enums for status and priority
class Status(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in-progress"
    CLOSED = "closed"

class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Database model
class IssueDB(Base):
    __tablename__ = "issues"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.OPEN)
    priority = Column(Enum(Priority), nullable=False, default=Priority.MEDIUM)
    assignee = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

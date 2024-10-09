import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLITE_DATABASE_URL = "sqlite:///./report.db"

engine = create_engine(
    SQLITE_DATABASE_URL,
    echo=False,  # Set to True for debugging
    pool_size=20,
    max_overflow=0,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_engine():
    return engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"An error occurred while connecting to the database: {e}")
        raise
    finally:
        db.close()

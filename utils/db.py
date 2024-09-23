from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./report.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_engine():
    return engine

def get_db():
    print("yoooo")
    db = SessionLocal()
    try:
        # Test the connection
        db.execute(text("SELECT 1"))
        print("Successfully connected to the database.")
        return db
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        raise
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Flag to toggle between PostgreSQL and SQLite
USE_POSTGRESQL = False  # Set to True if using PostgreSQL

# Database URLs for PostgreSQL and SQLite
POSTGRES_URL = "postgresql://postgres:password@localhost:5432/student_db"
SQLITE_URL = "sqlite:///./test.db"  # SQLite uses a file-based database


# Dynamically select the database based on the flag
DATABASE_URL = POSTGRES_URL if USE_POSTGRESQL else SQLITE_URL

# Create the database engine with appropriate connection settings
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Logs SQL queries for debugging
    connect_args={"check_same_thread": False} if not USE_POSTGRESQL else {}  # SQLite-specific config
)


# Session factory to manage database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    """Provides a database session instance, ensuring proper resource cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Close session after use

def init_db():
    """Initializes database tables based on defined SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)

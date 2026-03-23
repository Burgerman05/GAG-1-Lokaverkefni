from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.db_config import db_config

USER = db_config.db_username
PASSWORD = db_config.db_password
PORT = db_config.db_port
DATABASE_NAME = db_config.db_name

# Database connection string
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"

# Create the SQLAlchemy engine (handles the actual DB connection pool)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency function that provides a DB session
def get_orkuflaedi_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

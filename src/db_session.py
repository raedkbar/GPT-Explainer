import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


MODULE_DIR = Path(__file__).resolve().parent
DB_PATH = str(MODULE_DIR / ".." / "db" / "explainer.db")


def create_session():
    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        # Create an empty database file
        open(DB_PATH, 'w').close()
        print(f"Created empty database file: {DB_PATH}")

    # Create database connection
    engine = create_engine(f'sqlite:///{DB_PATH}')
    engine.echo = False
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return Session()

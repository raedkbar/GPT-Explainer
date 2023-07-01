import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Get the directory of the current module
MODULE_DIR = Path(__file__).resolve().parent

# Define the path to the database file
DB_PATH = str(MODULE_DIR / ".." / "db" / "explainer.db")


def create_session():
    """
    Create a session object for interacting with the database.

    Returns:
        Session: A session object bound to the database engine.
    """
    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        open(DB_PATH, 'w').close()
        print(f"Created empty database file: {DB_PATH}")

    # Create a connection to the database
    engine = create_engine(f'sqlite:///{DB_PATH}')
    engine.echo = False

    # Create the tables if they don't exist
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    return Session()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import sys

def get_db_path():
    """
    Get the database path. When running as executable, store it next to the exe.
    When running as script, store it in the project directory.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        # Store database in the same directory as the executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(base_path, "tracker.sqlite")
    return db_path

DB_NAME = get_db_path()
DB_URL = f"sqlite:///{DB_NAME}"

engine = create_engine(DB_URL, echo=False, future=True)
sessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush= False, autocommit=False)
)

def init_db(base):
    # create db file if missing
    if not os.path.exists(DB_NAME):
        # Ensure the directory exists
        db_dir = os.path.dirname(DB_NAME)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        open(DB_NAME,"a").close()
    base.metadata.create_all(bind=engine)

def get_session():
    return sessionLocal()
    

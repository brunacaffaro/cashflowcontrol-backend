"""Initializes the database connection and ORM models."""
import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Importing the elements defined in the model
from model.base import Base
from model.transaction import Transaction

DB_PATH = "database/"
# Checks if the directory exists
if not os.path.exists(DB_PATH):
   # then create the directory
    os.makedirs(DB_PATH)

# Database access URL (this is a local SQLite access URL)
DB_URL = f"sqlite:///{DB_PATH}/db.sqlite3"

# Create the database connection engine
engine = create_engine(DB_URL, echo=False)

# Create a session maker bound to the engine
Session = sessionmaker(bind=engine)

# Create the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)

# Create the database tables if they do not exist
Base.metadata.create_all(engine)

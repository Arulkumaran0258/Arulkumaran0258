from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Define your MySQL database connection URL
DB_URL = 'mysql+mysqlconnector://root:kirup#a1@localhost/EPSM1'

# Create the engine
engine = create_engine(DB_URL)

# Create the session class
Session = sessionmaker(bind=engine)

# Create the database tables if they don't exist
Base.metadata.create_all(engine)
 
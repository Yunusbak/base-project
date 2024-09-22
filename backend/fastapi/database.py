import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
load_dotenv()

base_info = os.getenv('DATABASE_INFO')

Engine = create_engine(f'{base_info}')

Base = declarative_base()
Session = sessionmaker()
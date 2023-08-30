from utils import play_match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

print(session.query(Match).count())
play_match(session=session, match=2)

session.close()

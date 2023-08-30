from utils import play_match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match


engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()

num_match = session.query(Match).count()
for i in range(1, 6):
    score_A, score_B, bonus_A, bonus_B = play_match(session=session, match=i)
    print(score_A, score_B, bonus_A, bonus_B)
session.close()

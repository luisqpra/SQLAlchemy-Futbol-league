from utils import play_match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match


engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()

num_match = session.query(Match).count()
for i in range(1, 12):
    teamM_A, teamM_B = session.query(Match).filter_by(num_match=i).all()
    score_A, score_B, bonus_A, bonus_B = play_match(session=session, match=i)
    print(score_A, score_B, bonus_A, bonus_B)
    # UPDATE SCORE AND BONUS TO FINISH IN MATCHES
    '''
    match_to_update = session.query(Match).filter_by(id=1).first()
    if match_to_update:
        match_to_update.team_score = 3
        match_to_update.bonus_defence = 1
        match_to_update.bonus_forward = 1
        match_to_update.bonus_midfielder = 1
        session.commit()
    '''
session.close()

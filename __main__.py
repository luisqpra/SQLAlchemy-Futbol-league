from utils import play_match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match


engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()

num_match = int(session.query(Match).count()/2)
print(num_match)
for i in range(1, 1+num_match):
    teamM_A, teamM_B = session.query(Match).filter_by(num_match=i).all()
    team_goals_A, bonus_A, team_goals_B, bonus_B = play_match(session=session,
                                                              match=i)
    print(f'match({i})', team_goals_A, '-', team_goals_B)
    print(bonus_A, bonus_B)

session.close()

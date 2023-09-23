from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match
# from models import Team
from sqlalchemy import create_engine

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()


if __name__ == '__main__':
    # teams = session.query(Team).delete()
    matchs = session.query(Match).delete()
    session.commit()
    print("Base de datos elimindada")
    session.close()

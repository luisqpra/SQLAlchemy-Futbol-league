from config import database_url
from models import Match
# from models import Team
from sqlalchemy import create_engine

engine = create_engine(database_url)

if __name__ == '__main__':
    # Team.__table__.drop(engine)
    Match.__table__.drop(engine)
    print("Base de datos elimindada")
    engine.dispose()

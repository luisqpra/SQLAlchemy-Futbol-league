from config import database_url
from utils import (insert_teams_with_random_stats,
                   get_team_ids, create_season)
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Match
from models import Team

# Creamos un motor de base de datos usando la URL y habilitamos la opción
# de impresión de comandos SQL (echo)
engine = create_engine(database_url)

# Crea un objeto Inspector para inspeccionar la base de datos
inspector = inspect(engine)

# Creamos una clase Session que se utilizará para interactuar con la base
# de datos
Session = sessionmaker(bind=engine)
session = Session()

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Obtiene una lista de todas las tablas en la base de datos
tabla_names = inspector.get_table_names()

# Crear los equipos
harry_potter_teams = [
    "Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw",
    "Quidditch Crushers", "Phoenix Flyers", "Broomstick Blazers",
    "Wizarding Warriors", "Spellcast Strikers", "Enchanted Defenders"
]

season = 2


# Verifica si las tablas de Match y Team están en la lista de tablas
if 'teams' in tabla_names and session.query(Team).count() == 0:
    insert_teams_with_random_stats(harry_potter_teams, session=session)
    print("Los equipos se han sido creados.")
else:
    print("Los equipos ya han sido creados.")

if 'matches' in tabla_names and session.query(Match).count() == 0:
    # Crear el calendario Fixture
    list_IDteams = get_team_ids(session)
    create_season(teams=list_IDteams, session=session, seasons=season)
    session.close()
    print("Los partidos se han sido creados.")
else:
    print("Los partidos ya han sido creados.")

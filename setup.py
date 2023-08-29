from config import database_url
from utils import insert_teams_with_random_stats, get_team_ids, create_season
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Creamos un motor de base de datos usando la URL y habilitamos la opción
# de impresión de comandos SQL (echo)
engine = create_engine(database_url, echo=True)

# Creamos una clase Session que se utilizará para interactuar con la base
# de datos
Session = sessionmaker(bind=engine)
session = Session()

# Crear las tablas en la base de datos
# from models import Base
# Base.metadata.create_all(engine)

# Crear los equipos
harry_potter_teams = [
    "Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw",
    "Quidditch Crushers", "Phoenix Flyers", "Broomstick Blazers",
    "Wizarding Warriors", "Spellcast Strikers", "Enchanted Defenders"
]

# Ingresar equipos a la base de datos
insert_teams_with_random_stats(harry_potter_teams, session=session)

# Crear el calendario Fixture
list_IDteams = get_team_ids(session)
matches = create_season(teams=list_IDteams, session=session)

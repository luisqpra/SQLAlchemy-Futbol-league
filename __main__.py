from models import Base
from config import engine

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

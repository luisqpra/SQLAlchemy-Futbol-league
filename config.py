# Importamos el módulo os y sqlalchemy para su uso en el código
import os

# Nombre del archivo de la base de datos SQLite
sqlite_file_name = "database.sqlite"

# Obtenemos la ruta absoluta del directorio actual del archivo de script
base_dir = os.path.dirname(os.path.realpath(__file__))

# Creamos la URL de la base de datos usando la ruta absoluta y el nombre
# del archivo
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Numero de temporadas
season = 2

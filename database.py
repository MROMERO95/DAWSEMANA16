import sqlite3
from pathlib import Path


# Ruta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carpeta donde se almacenará la base de datos
DATA_DIR = BASE_DIR / "data"

# Archivo de base de datos SQLite
DB_PATH = DATA_DIR / "parqueadero.db"


def inicializar_db():
    # Crear la carpeta data si no existe
    DATA_DIR.mkdir(exist_ok=True)

    # Establecer conexión con la base de datos
    conn = sqlite3.connect(DB_PATH)

    # Crear la tabla productos si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL,
            disponible INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def obtener_productos():
    # Establecer conexión
    conn = sqlite3.connect(DB_PATH)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    # Ejecutar consulta
    productos = conn.execute("""
        SELECT * FROM productos
    """).fetchall()

    # Cerrar conexión
    conn.close()

    # Devolver los productos
    return productos
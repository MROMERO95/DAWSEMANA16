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
    # Crear la tabla clientes si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cedula TEXT NOT NULL,
            telefono TEXT NOT NULL,
            placa TEXT NOT NULL
        )
    """)
    # Crear la tabla proveedores si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            servicio TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)
        # Crear la tabla facturacion si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facturacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            cliente TEXT NOT NULL,
            placa TEXT NOT NULL,
            servicio TEXT NOT NULL,
            horas INTEGER NOT NULL,
            total REAL NOT NULL
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

def obtener_clientes():
    # Establecer conexión
    conn = sqlite3.connect(DB_PATH)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    # Ejecutar consulta
    clientes = conn.execute("""
        SELECT * FROM clientes
    """).fetchall()

    # Cerrar conexión
    conn.close()

    # Devolver los clientes
    return clientes

def obtener_proveedores():
    # Establecer conexión
    conn = sqlite3.connect(DB_PATH)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    # Ejecutar consulta
    proveedores = conn.execute("""
        SELECT * FROM proveedores
    """).fetchall()

    # Cerrar conexión
    conn.close()

    # Devolver los proveedores
    return proveedores

def obtener_facturas():
    # Establecer conexión
    conn = sqlite3.connect(DB_PATH)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    # Ejecutar consulta
    facturas = conn.execute("""
        SELECT * FROM facturacion
    """).fetchall()

    # Cerrar conexión
    conn.close()

    # Devolver las facturas
    return facturas


from pathlib import Path
import sqlite3


# Ruta de la base de datos
DB_PATH = Path(__file__).parent.absolute() / "gespagos.db"


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    # -------------------------
    # Métodos básicos
    # -------------------------

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)


    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()


# estructura de la base de datos donde se define sus relaciones y sus camps 

def estructure_db(database: Database):
    cursor = database.cursor

    # usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        uuid INTEGER NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # deudas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS debts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total INTEGER,
        total_paid INTEGER,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # abonos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        debt_id INTEGER,
        amount INTEGER,
        date TEXT,
        FOREIGN KEY(debt_id) REFERENCES debts(id)
    )
    """)

    database.commit()


# -------------------------
# Inicialización automática
# -------------------------

def init_db():
    # Crear archivo si no existe
    if not DB_PATH.exists():
        DB_PATH.touch()

    db = Database(DB_PATH)
    estructure_db(db)
    return db


# instancia lista para usar
db = init_db()

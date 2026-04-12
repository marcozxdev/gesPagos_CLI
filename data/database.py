
from pathlib import Path



# ruta donde puede estar la base de datos 
db = Path(__file__).parent.absolute() / "gespagos.db"




import sqlite3




def estructure_db(db):
    
    '''crea la estructura de la bd
        tablas (usuarios, deudas, abonos)
        y sus campos por tabla
    '''

    # conexion con la bd 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()



    # extructura de las tablas 

    # usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY ,
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


    # cerramos la conexion 
    conn.commit()




# conexion con la bd 
conn = sqlite3.connect(db)
cursor = conn.cursor()





if db.exists() and db.is_file():
    estructure_db(db)
else:
    with open(db, "w") as f:
        f.close()
        
    estructure_db(db)



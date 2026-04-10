
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
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY ,
        uuid INTEGER NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        contraseña TEXT NOT NULL
    )
    """)


    # deudas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deudas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        total REAL,
        descripcion TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)

    # abonos 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS abonos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deuda_id INTEGER,
        monto REAL,
        fecha TEXT,
        FOREIGN KEY(deuda_id) REFERENCES deudas(id)
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



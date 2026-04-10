

from repository.sqlite_repo import Sqlite
from model.models import Usuario, Deuda, Abono



database = Sqlite()

# prepara las consultas de usuario 
class UsuarioRepo(Usuario):

    # obtiene el primer usuario con la concidencia
    def get_user(self, email):
        database.cursor.execute("""SELECT * FROM usuarios
                                    WHERE email = ? """, (email,))
        user = database.cursor.fetchall()
        return user
    

    # crea un usuario nuevo 
    def new_user(self):
        
        # valida que el usuario exista para no crearlo
        if self.get_user(self.email):
            return False

        database.cursor.execute("""INSERT INTO usuarios (uuid, email, nombre, contraseña)
                                    VALUES (?, ?, ?, ?)""", (self.uuid, self.email ,self.nombre, self.contraseña,))
        database.conn.commit()
        
        return True


# consultas de deudas 
class DeudaRepo(Deuda):
    
    
    def  user_deudas(self, useruuid):
        database.cursor.execute("""SELECT * FROM deudas d
                                INNER JOIN usuarios u ON d.usuario_id = u.id
                                WHERE u.uuid = ? """, (useruuid,))




# consultas sobre abonos
class AbonoRepo(Abono):
    

    def abonos(self):
        database.cursor.execute(""" """)
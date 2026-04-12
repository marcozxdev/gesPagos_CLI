from repository.sqlite_repo import Sqlite
from model.models import User, Debt, Payments

database = Sqlite()


# prepara las consultas de usuario 
class UserRepo(User):

    # obtiene el primer usuario con la coincidencia
    def get_user(self, email):
        database.cursor.execute("""SELECT * FROM users
                                    WHERE email = ? """, (email,))
        user = database.cursor.fetchone()
        return user
    

    # crea un usuario nuevo 
    def new_user(self):
        
        # valida que el usuario exista para no crearlo
        if self.get_user(self.email):
            return False

        database.cursor.execute("""INSERT INTO users (uuid, email, name, password)
                                    VALUES (?, ?, ?, ?)""",
                                    (self.uuid, self.email, self.name, self.password,))
        
        database.conn.commit()
        
        return True


# consultas de deudas 
class DebtRepo(Debt):
    
    # lista las deudas de un usuario 
    def user_debts(self, user_id):
        database.cursor.execute("""SELECT * FROM debts d
                                INNER JOIN users u ON d.user_id = u.id
                                WHERE u.id = ? """, (user_id,))
        debts = database.cursor.fetchall()

        if not debts:
            return False
        
        return debts


# consultas sobre abonos
class PaymentsRepo(Payments):
    
    # lista los abonos de una deuda 
    def list_payments(self, usuario_id, deuda_id):
        database.cursor.execute("""SELECT  p.id as abono_id, p.debt_id, d.user_id, d.description, p.amount, p.date FROM debts d
                                    INNER JOIN payments p ON p.debt_id = d.id
                                    INNER JOIN users u on u.id = d.user_id
                                    WHERE d.user_id = ? and d.id = ? """, (usuario_id, deuda_id,))
        
        payments = database.cursor.fetchall()

        if not payments:
            return False
        
        return payments

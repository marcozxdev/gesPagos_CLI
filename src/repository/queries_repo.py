from src.data.database import Database




class UserRepo:
    def __init__(self, db: Database):
        self.database = db

    def get_user(self, email: str):
        self.database.execute("""
            SELECT * FROM users
            WHERE email = :email
        """, {"email": email})

        return self.database.fetchone()

    def new_user(self, uuid: int, email: str, name: str, password: str) -> bool:
        if self.get_user(email):
            return False

        self.database.execute("""
            INSERT INTO users (uuid, email, name, password)
            VALUES (:uuid, :email, :name, :password)
        """, {
            "uuid": uuid,
            "email": email,
            "name": name,
            "password": password
        })

        return True




class DebtRepo:
    def __init__(self, db: Database):
        self.database = db

    def add_debt(self, user_id: int, total: int, description: str) -> None:
        self.database.execute("""
            INSERT INTO debts (user_id, total, total_paid, description)
            VALUES (:user_id, :total, 0, :description)
        """, {
            "user_id": user_id,
            "total": total,
            "description": description
        })

    def count_debts(self, user_id: int) -> int:
        self.database.execute("""
            SELECT COUNT(*) FROM debts
            WHERE user_id = :user_id
        """, {"user_id": user_id})

        result = self.database.fetchone()
        return result[0] if result else 0

    def total_debts(self, user_id: int) -> int:
        self.database.execute("""
            SELECT SUM(total) FROM debts
            WHERE user_id = :user_id
        """, {"user_id": user_id})

        result = self.database.fetchone()
        return result[0] if result and result[0] else 0

    def user_debts(self, user_id: int):
        self.database.execute("""
            SELECT * FROM debts
            WHERE user_id = :user_id
        """, {"user_id": user_id})

        return self.database.fetchall()




class PaymentsRepo:
    def __init__(self, db: Database):
        self.database = db

    def add_payment(self, debt_id: int, amount: int, date: str) -> None:
        # insertar pago
        self.database.execute("""
            INSERT INTO payments (debt_id, amount, date)
            VALUES (:debt_id, :amount, :date)
        """, {
            "debt_id": debt_id,
            "amount": amount,
            "date": date
        })

        # actualizar deuda
        self.database.execute("""
            UPDATE debts
            SET total_paid = total_paid + :amount
            WHERE id = :debt_id
        """, {
            "amount": amount,
            "debt_id": debt_id
        })

    def list_payments(self, user_id: int, debt_id: int):
        self.database.execute("""
            SELECT p.id, p.debt_id, p.amount, p.date
            FROM payments p
            INNER JOIN debts d ON p.debt_id = d.id
            WHERE d.user_id = :user_id AND d.id = :debt_id
        """, {
            "user_id": user_id,
            "debt_id": debt_id
        })

        return self.database.fetchall()

from src.repository.queries_repo import UserRepo, DebtRepo, PaymentsRepo
from src.utils.utils import encrypte_password, valide_pasword, get_current_date
from src.data.database import Database




class UserService:
    def __init__(self, repo: UserRepo, db: Database):
        self.repo = repo
        self.db = db

    def register_user(self, uuid: int, email: str, name: str, password: str):
        if not (uuid and email and name and password):
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        try:
            secure_password = encrypte_password(password)
            is_register = self.repo.new_user(uuid, email, name, secure_password)

            if not is_register:
                return False

            self.db.commit()
            return "USUARIO CREADO EXITOSAMENTE"

        except:
            self.db.rollback()
            raise  

    def log_user(self, email: str, password: str):
        if not (email and password):
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        user = self.repo.get_user(email)

        if not user:
            return False

        # user[4] porque fetchone devuelve una fila (no lista de filas)
        is_user = valide_pasword(password, user[4])

        return user if is_user else False




class DebtService:
    def __init__(self, repo: DebtRepo, db: Database):
        self.repo = repo
        self.db = db

    def add_debt(self, user_id: int, total: int, description: str):
        if not (user_id and total and description):
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        try:
            self.repo.add_debt(user_id, total, description)
            self.db.commit()
            return "DEUDA AÑADIDA"

        except:
            self.db.rollback()
            raise

    def list_debts(self, user_id: int):
        if not user_id:
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        return self.repo.user_debts(user_id)

    def list_total_debts(self, user_id: int):
        if not user_id:
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        return self.repo.total_debts(user_id)

    def count_debts(self, user_id: int):
        if not user_id:
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        return self.repo.count_debts(user_id)




class PaymentService:
    def __init__(self, repo: PaymentsRepo, db: Database):
        self.repo = repo
        self.db = db

    def add_payment(self, debt_id: int, amount: int):
        if not (debt_id and amount):
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        try:
            date = get_current_date()
            self.repo.add_payment(debt_id, amount, date)
            self.db.commit()
            return f"ABONO: {amount} A LA DEUDA N°: {debt_id}"

        except:
            self.db.rollback()
            raise

    def list_payments(self, user_id: int, debt_id: int):
        if not (user_id and debt_id):
            return "ASEGURESE DE INGRESAR BIEN LOS DATOS"

        return self.repo.list_payments(user_id, debt_id)

    





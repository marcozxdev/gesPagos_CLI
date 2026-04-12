from repository.queries_repo import UserRepo, DebtRepo, PaymentsRepo
from utils.utils import encrypte_password, valide_pasword

# logica de los service de los usuarios 
class UserService(UserRepo):

    # valida el que consida el usuario
    def valide_user(self):
        is_user = self.get_user(self.email)






# logica de las deuadas 
class DebtService(DebtRepo):
    pass



# logica de los pagos o abonos
class PaymentService(PaymentsRepo):
    pass





from src.repository.sqlite_repo import Sqlite
from src.repository.queries_repo import UserRepo, DebtRepo, PaymentsRepo
from src.service.service import UserService, DebtService, PaymentService
from src.cli.cli import run_cli

def main():
    
    # Inicializar DB
    db = Sqlite()

    # Inicializar repos
    user_repo = UserRepo(db)
    debt_repo = DebtRepo(db)
    payments_repo = PaymentsRepo(db)



    # Inicializar servicios
    user_service = UserService(user_repo, db)
    debt_service = DebtService(debt_repo, db)
    payment_service = PaymentService(payments_repo, db)

   
    # EJECUCIÓN PRINCIPAL
    run_cli(user_service, debt_service, payment_service)
   



# ENTRY POINT
main()

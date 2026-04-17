
"""Models se encarga de definir los objetos para la bd"""

 

# modelado de los datos para la base de datos

class User:
    def __init__(self, uuid: int, email: str, name: str, password: str):
        self.uuid = uuid
        self.email = email
        self.name = name
        self.password = password




class Debt:
    def __init__(self, user_id: int, total: int, total_paid: int, description: str):
        self.user_id = user_id
        self.total = total
        self.total_paid = total_paid = 0
        self.description = description






class Payments:
    def __init__(self, debt_id: int, amount: int, date: str):
        self.debt_id = debt_id
        self.amount = amount 
        self.date = date



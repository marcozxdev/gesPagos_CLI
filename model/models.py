
"""Models se encarga de definir los objetos para la bd"""

 

# modelado de los datos para la base de datos

class Usuario:
    def __init__(self, uuid: int, email: str, nombre: str, contraseña: str):
        self.uuid = uuid
        self.email = email
        self.nombre = nombre
        self.contraseña = contraseña




class Deuda:
    def __init__(self, usuario_id: int, total: float, descripcion: str ):
        self.usuario_id = usuario_id
        self.total = total
        self.descripcion = descripcion





class Abono:
    def __init__(self, deuda_id: int, monto: float, fecha: str):
        self.deuda_id = deuda_id
        self.monto = monto 
        self.fecha = fecha



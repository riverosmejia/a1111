class Usuario:
    def __init__(self, nombre, contraseña, monto, grupos=None):
        self.nombre = nombre
        self.contraseña = contraseña
        self.monto =monto
        self.deuda = 0
        self.Grupos = grupos if grupos is not None else [] 

    def __str__(self):
        return f'nombre: {self.nombre} --> contraseña: {self.contraseña} --> cantidad de dinero: {self.monto} --> Grupos: {self.Grupos}'

    def get_nombre(self):
        return self.nombre

    def get_contraseña(self):
        return self.contraseña

    def obtener_info(self):
        grupos_str = ", ".join(self.Grupos)
        return f"Nombre: {self.nombre} Contraseña: {self.contraseña} Monto: {self.monto} Grupos: {grupos_str}"


class Paciente:
    
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self.__nombre__ = nombre
        self.__dni__ = dni
        self.__fecha_nacimiento__ = fecha_nacimiento
    
    def obtener_dni(self) -> str:
        return self.__dni__
    
    def __str__(self) -> str:
        return f"Paciente: {self.__nombre__} | DNI: {self.__dni__} | Fecha de Nacimiento: {self.__fecha_nacimiento__}"

from models.Paciente import Paciente
from models.Turno import Turno
from models.Receta import Receta
class HistoriaClinica:
    def __init__(self, paciente,):
        self.__paciente__ = paciente
        self.__turnos__:list[Turno] = []
        self.__recetas__:list[Receta] = []
    
    def agregar_turno(self, turno):
        self.__turnos__.append(turno)
    
    def agregar_receta(self, receta:Receta):

        self.__recetas__.append(receta)
    
    def obtener_turnos(self):

        return self.__turnos__
    
    def obtener_recetas(self):
        return self.__recetas__
    
    def __str__(self):
        
        resultado = f"=== HISTORIA CLÍNICA ===\n"
        resultado += f"Paciente: {self.__paciente__}\n"
        resultado += f"Número de turnos: {len(self.__turnos__)}\n"
        resultado += f"Número de recetas: {len(self.__recetas__)}\n\n"
        
        if self.__turnos__:
            resultado += "--- TURNOS ---\n"
            for i, turno in enumerate(self.__turnos__, 1):
                resultado += f"{i}. {turno}\n"
        else:
            resultado += "--- TURNOS ---\nNo hay turnos registrados.\n"
        
        resultado += "\n"
        
        if self.__recetas__:
            resultado += "--- RECETAS ---\n"
            for i, receta in enumerate(self.__recetas__, 1):
                resultado += f"{i+1}. {receta}\n"
        else:
            resultado += "--- RECETAS ---\nNo hay recetas registradas.\n"
        
        return resultado
    
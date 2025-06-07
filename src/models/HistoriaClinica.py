from Paciente import Paciente
from Turno import Turno
from Receta import Receta
class HistoriaClinica:
    def __init__(self, paciente,):
        self.__paciente__ = paciente
        self.__turnos__:list[Turno] = []
        self.__recetas__:list[Receta] = []
    
    def agregar_turno(self, turno):
        self.__turnos.append(turno)
    
    def agregar_receta(self, receta):

        self.__recetas.append(receta)
    
    # 📄 Acceso a Información
    def obtener_turnos(self):

        return self.__turnos
    
    def obtener_recetas(self):
        return self.__recetas
    
    def __str__(self):
        
        resultado = f"=== HISTORIA CLÍNICA ===\n"
        resultado += f"Paciente: {self.__paciente}\n"
        resultado += f"Número de turnos: {len(self.__turnos)}\n"
        resultado += f"Número de recetas: {len(self.__recetas)}\n\n"
        
        if self.__turnos:
            resultado += "--- TURNOS ---\n"
            for i, turno in enumerate(self.__turnos, 1):
                resultado += f"{i}. {turno}\n"
        else:
            resultado += "--- TURNOS ---\nNo hay turnos registrados.\n"
        
        resultado += "\n"
        
        if self.__recetas:
            resultado += "--- RECETAS ---\n"
            for i, receta in enumerate(self.__recetas, 1):
                resultado += f"{i+1}. {receta}\n"
        else:
            resultado += "--- RECETAS ---\nNo hay recetas registradas.\n"
        
        return resultado
    
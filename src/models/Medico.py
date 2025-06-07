from Especialidad import Especialidad
class Medico:
    
    def __init__(self, nombre: str, matricula: str):
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__:list[Especialidad] = []
    
    def agregar_especialidad(self, especialidad:Especialidad) -> None:

        self.__especialidades__.append(especialidad)
    
    def obtener_matricula(self) -> str:
        return self.__matricula__
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidades__:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_nombre()
        return None
from src.models.Especialidad import Especialidad
class Medico:
    
    def __init__(self, nombre: str, matricula: str):
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__:list[Especialidad] = []
    
    def agregar_especialidad(self, especialidad:Especialidad) -> None:
        for i in especialidad.obtener_dias():
            self.validar_dia(dia=i)
        if especialidad.obtener_especialidad() in [e.obtener_especialidad() for e in self.__especialidades__ ]:
            raise ValueError('Especialidad repetida')
        self.__especialidades__.append(especialidad)
    
    def obtener_matricula(self) -> str:
        return self.__matricula__
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidades__:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None

    def validar_dia(self,dia:str)-> None:
        dia = dia.lower()
        if dia!='lunes' and dia !='martes' and dia !='miercoles' and dia !='miércoles' and dia != 'jueves' and dia !='viernes' and dia !='sabado' and dia != 'domingo':
            raise ValueError('dia invalido') 
    def __str__(self):
        return f"Nombre:{self.__nombre__}, matricula: {self.__matricula__} especialidades: {','.join([e.obtener_especialidad() for e in self.__especialidades__ ])}"
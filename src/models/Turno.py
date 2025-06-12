from src.models.Paciente import Paciente
from src.models.Medico import Medico
from datetime import datetime

class Turno():
    def __init__(self,paciente:Paciente,medico:Medico,fecha_hora:datetime,especialidad:str):
        self.__paciente__:Paciente =paciente
        self.__medico__:Medico = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad

    def obtener_medico(self) -> Medico:
        return self.__medico__
    def obtener_fecha_hora(self) ->datetime:
        return self.__fecha_hora__
    def __str__(self):
        return f'Paciente:{self.__paciente__.__nombre__} , medico: {self.__medico__.__nombre__}, fecha y hora: {self.__fecha_hora__}, especialidad {self.__especialidad__}'
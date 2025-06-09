from src.models.Medico import Medico
from src.models.Paciente import Paciente
from datetime import datetime

class Receta():
    def __init__(self,paciente:Paciente, medicamentos:list[str], medico:Medico):
        self.__paciente__ = paciente
        self.__medicamentos__= medicamentos
        self.__medico__= medico
        self.__fecha__= datetime.now()

    def __str__(self):
        return f'Paciente: {self.__paciente__}, Medicamentos: {self.__medicamentos__}, Medico: {self.__medico__}, fecha: {self.__fecha__}'
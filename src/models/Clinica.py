from datetime import datetime
from typing import Dict, List
from src.models.Paciente import Paciente
from src.models.Medico import Medico
from src.models.Turno import Turno
from src.models.Receta import Receta
from src.models.HistoriaClinica import HistoriaClinica
from src.exceptions.MedicoNoDisponibleException import MedicoNoDisponibleException
from src.exceptions.PacienteNoEncontradoException import PacienteNoEncontradoException
from src.exceptions.RecetaInvalidaException import RecetaInvalidaException
from src.exceptions.TurnoOcupadoException import TurnoOcupadoException


class Clinica:
    def __init__(self):
        
        self.__pacientes__: Dict[str, 'Paciente'] = {}
        self.__medicos__: Dict[str, 'Medico'] = {}
        self.__turnos__: List['Turno'] = []
        self.__historias_clinicas__: Dict[str, 'HistoriaClinica'] = {}
    
    def agregar_paciente(self, paciente: 'Paciente') -> None:

        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise ValueError(f"El paciente con DNI {dni} ya está registrado")
        
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)
    
    def agregar_medico(self, medico: 'Medico') -> None:

        matricula = medico.obtener_matricula()
        if matricula in self.__medicos__:
            raise ValueError(f"El médico con matrícula {matricula} ya está registrado")
        
        self.__medicos__[matricula] = medico
    
    def obtener_pacientes(self) -> List['Paciente']:
        return list(self.__pacientes__.values())
    
    
    def obtener_medicos(self) -> List['Medico']:

        return list(self.__medicos__.values())
    
    def obtener_medico_por_matricula(self, matricula: str) -> 'Medico':

        self.validar_existencia_medico(matricula)
        return self.__medicos__[matricula]
    
    
    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime) -> None:

        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)
        
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        
        nuevo_turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(nuevo_turno)
        
        self.__historias_clinicas__[dni].agregar_turno(nuevo_turno)
    
    def obtener_turnos(self) -> List['Turno']:    
        return self.__turnos__.copy()
    

    def emitir_receta(self, dni: str, matricula: str, medicamentos: List[str]) -> None:
        
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        if not medicamentos:
            raise RecetaInvalidaException("La receta debe contener al menos un medicamento")
        
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        
        nueva_receta = Receta(paciente, medicamentos, medico)
        
        self.__historias_clinicas__[dni].agregar_receta(nueva_receta)
    
    def obtener_historia_clinica(self, dni: str) -> 'HistoriaClinica':
        
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas__[dni]
    
    
    def validar_existencia_paciente(self, dni: str) -> None:
        
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"No se encontró paciente con DNI: {dni}")
    
    def validar_existencia_medico(self, matricula: str) -> None:
        
        if matricula not in self.__medicos__:
            raise MedicoNoDisponibleException(f"No se encontró médico con matrícula: {matricula}")
    
    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime) -> None:
        for turno in self.__turnos__:
            if (turno.obtener_medico().obtener_matricula() == matricula and turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoOcupadoException(f"El médico ya tiene un turno agendado el {fecha_hora.strftime('%d/%m/%Y %H:%M')}")
    
    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:

        dias_semana = {
            0: "lunes",
            1: "martes", 
            2: "miercoles",
            3: "jueves",
            4: "viernes",
            5: "sabado",
            6: "domingo"
        }
        return dias_semana[fecha_hora.weekday()]
    
    
    def validar_especialidad_en_dia(self, medico: 'Medico', especialidad_solicitada: str, dia_semana: str) -> None:
        try:
            especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
            if especialidad_disponible ==None:
                raise MedicoNoDisponibleException(f"El médico no atiende esa especialidad ")
            if especialidad_disponible.lower() != especialidad_solicitada.lower():
                raise MedicoNoDisponibleException(f"El médico no atiende {especialidad_solicitada} los {dia_semana}. ")
        except Exception as e:
            raise e
    
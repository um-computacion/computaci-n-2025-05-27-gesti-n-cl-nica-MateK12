from datetime import datetime
from typing import Dict, List
from Paciente import Paciente
from Medico import Medico
from Turno import Turno
from HistoriaClinica import HistoriaClinica
from exceptions.MedicoNoDisponibleException import MedicoNoDisponibleException
from exceptions.PacienteNoEncontradoException import PacienteNoEncontradoException
from exceptions.RecetaInvalidaException import RecetaInvalidaException
from exceptions.TurnoOcupadoException import TurnoOcupadoException


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
        """
        Devuelve todos los médicos registrados.
        
        Returns:
            list[Medico]: Lista de todos los médicos
        """
        return list(self.__medicos.values())
    
    def obtener_medico_por_matricula(self, matricula: str) -> 'Medico':
        """
        Devuelve un médico por su matrícula.
        
        Args:
            matricula (str): Matrícula del médico
        
        Returns:
            Medico: El médico correspondiente
        
        Raises:
            MedicoNoEncontradoException: Si no se encuentra el médico
        """
        self.validar_existencia_medico(matricula)
        return self.__medicos[matricula]
    
    # 📆 Turnos
    
    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime) -> None:
        """
        Agenda un turno si se cumplen todas las condiciones.
        
        Args:
            dni (str): DNI del paciente
            matricula (str): Matrícula del médico
            especialidad (str): Especialidad solicitada
            fecha_hora (datetime): Fecha y hora del turno
        
        Raises:
            PacienteNoEncontradoException: Si no existe el paciente
            MedicoNoDisponibleException: Si el médico no está disponible
            TurnoOcupadoException: Si el turno ya está ocupado
        """
        # Validar existencia de paciente y médico
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        # Obtener día de la semana
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        
        # Validar que el médico atienda esa especialidad ese día
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)
        
        # Validar que no haya turno duplicado
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        
        # Crear y agregar el turno
        from turno import Turno  # Importación local
        nuevo_turno = Turno(paciente, medico, especialidad, fecha_hora)
        self.__turnos.append(nuevo_turno)
        
        # Agregar turno a la historia clínica del paciente
        self.__historias_clinicas[dni].agregar_turno(nuevo_turno)
    
    def obtener_turnos(self) -> List['Turno']:
        """
        Devuelve todos los turnos agendados.
        
        Returns:
            list[Turno]: Lista de todos los turnos
        """
        return self.__turnos.copy()
    
    # 📑 Recetas e Historias Clínicas
    
    def emitir_receta(self, dni: str, matricula: str, medicamentos: List[str]) -> None:
        """
        Emite una receta para un paciente.
        
        Args:
            dni (str): DNI del paciente
            matricula (str): Matrícula del médico
            medicamentos (list[str]): Lista de medicamentos
        
        Raises:
            PacienteNoEncontradoException: Si no existe el paciente
            MedicoNoEncontradoException: Si no existe el médico
            RecetaInvalidaException: Si la receta no es válida
        """
        # Validar existencia de paciente y médico
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        # Validar que la lista de medicamentos no esté vacía
        if not medicamentos:
            from excepciones import RecetaInvalidaException
            raise RecetaInvalidaException("La receta debe contener al menos un medicamento")
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        # Crear y agregar la receta
        from receta import Receta  # Importación local
        nueva_receta = Receta(paciente, medico, medicamentos, datetime.now())
        
        # Agregar receta a la historia clínica del paciente
        self.__historias_clinicas[dni].agregar_receta(nueva_receta)
    
    def obtener_historia_clinica(self, dni: str) -> 'HistoriaClinica':
        """
        Devuelve la historia clínica completa de un paciente.
        
        Args:
            dni (str): DNI del paciente
        
        Returns:
            HistoriaClinica: Historia clínica del paciente
        
        Raises:
            PacienteNoEncontradoException: Si no existe el paciente
        """
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas[dni]
    
    # ✅ Validaciones y Utilidades
    
    def validar_existencia_paciente(self, dni: str) -> None:
        """
        Verifica si un paciente está registrado.
        
        Args:
            dni (str): DNI del paciente
        
        Raises:
            PacienteNoEncontradoException: Si el paciente no existe
        """
        if dni not in self.__pacientes:
            from excepciones import PacienteNoEncontradoException
            raise PacienteNoEncontradoException(f"No se encontró paciente con DNI: {dni}")
    
    def validar_existencia_medico(self, matricula: str) -> None:
        """
        Verifica si un médico está registrado.
        
        Args:
            matricula (str): Matrícula del médico
        
        Raises:
            MedicoNoEncontradoException: Si el médico no existe
        """
        if matricula not in self.__medicos:
            from excepciones import MedicoNoDisponibleException
            # Usamos MedicoNoDisponibleException ya que no existe MedicoNoEncontradoException
            raise MedicoNoDisponibleException(f"No se encontró médico con matrícula: {matricula}")
    
    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime) -> None:
        """
        Verifica que no haya un turno duplicado.
        
        Args:
            matricula (str): Matrícula del médico
            fecha_hora (datetime): Fecha y hora del turno
        
        Raises:
            TurnoOcupadoException: Si ya existe un turno en esa fecha y hora
        """
        for turno in self.__turnos:
            if (turno.medico.matricula == matricula and 
                turno.fecha_hora == fecha_hora):
                from excepciones import TurnoOcupadoException
                raise TurnoOcupadoException(
                    f"El médico ya tiene un turno agendado el {fecha_hora.strftime('%d/%m/%Y %H:%M')}"
                )
    
    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        """
        Traduce un objeto datetime al día de la semana en español.
        
        Args:
            fecha_hora (datetime): Fecha y hora
        
        Returns:
            str: Día de la semana en español
        """
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
    
    def obtener_especialidad_disponible(self, medico: 'Medico', dia_semana: str) -> str:
        """
        Obtiene la especialidad disponible para un médico en un día.
        
        Args:
            medico (Medico): El médico
            dia_semana (str): Día de la semana
        
        Returns:
            str: Especialidad disponible
        
        Raises:
            MedicoNoDisponibleException: Si el médico no trabaja ese día
        """
        horarios = medico.obtener_horarios()
        if dia_semana not in horarios:
            from excepciones import MedicoNoDisponibleException
            raise MedicoNoDisponibleException(
                f"El médico {medico.nombre} no trabaja los {dia_semana}"
            )
        
        return horarios[dia_semana]["especialidad"]
    
    def validar_especialidad_en_dia(self, medico: 'Medico', especialidad_solicitada: str, dia_semana: str) -> None:
        """
        Verifica que el médico atienda esa especialidad ese día.
        
        Args:
            medico (Medico): El médico
            especialidad_solicitada (str): Especialidad solicitada
            dia_semana (str): Día de la semana
        
        Raises:
            MedicoNoDisponibleException: Si el médico no atiende esa especialidad ese día
        """
        try:
            especialidad_disponible = self.obtener_especialidad_disponible(medico, dia_semana)
            if especialidad_disponible.lower() != especialidad_solicitada.lower():
                from excepciones import MedicoNoDisponibleException
                raise MedicoNoDisponibleException(
                    f"El médico {medico.nombre} no atiende {especialidad_solicitada} los {dia_semana}. "
                    f"Disponible: {especialidad_disponible}"
                )
        except Exception as e:
            # Re-lanzar la excepción si ya es del tipo correcto
            raise e
    
    def __str__(self) -> str:
        """
        Representación textual del sistema de la clínica.
        
        Returns:
            str: Resumen del estado del sistema
        """
        return f"""=== SISTEMA DE GESTIÓN CLÍNICA ===
Pacientes registrados: {len(self.__pacientes)}
Médicos registrados: {len(self.__medicos)}
Turnos agendados: {len(self.__turnos)}
Historias clínicas: {len(self.__historias_clinicas)}"""
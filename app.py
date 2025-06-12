from src.models.Clinica import Clinica
from src.models.Paciente import Paciente
from src.models.Medico import Medico
from src.models.Turno import Turno
from src.models.Receta import Receta
from datetime import datetime
from src.models.Especialidad import Especialidad
from src.exceptions.MedicoNoDisponibleException import MedicoNoDisponibleException
from src.exceptions.PacienteNoEncontradoException import PacienteNoEncontradoException
from src.exceptions.RecetaInvalidaException import RecetaInvalidaException
from src.exceptions.TurnoOcupadoException import TurnoOcupadoException




class CLI():

    def __init__(self):
        self.clinica =Clinica()

    def agregar_paciente(self):
        nombre = input('Ingrese el nombre del paciente: ')
        dni = input('Ingrese el dni del paciente: ')
        nacimiento = input('Ingrese la fecha de nacimiento del paciente: ')
        paciente = Paciente(nombre,dni,nacimiento)
        self.clinica.agregar_paciente(paciente)
        print('Paciente agregado con exito!!')
        print(paciente)
    
    def agregar_medico(self):
        nombre = input('Ingrese el nombre del medico: ')
        matricula = input('Ingrese la matricula del medico: ')
        medico = Medico(nombre,matricula)
        self.clinica.agregar_medico(medico)
        print('Medico agregado con exito!!')
        print(medico)
    
    def agendar_turno(self):
        dni = input('Ingrese dni del paciente: ')
        matricula = input('Ingrese la matricula del medico: ')
        especialidad = input('Ingrese la especialidad del medico: ')
        fecha = input('Ingrese la fecha y hora (dd-mm-yyyy hh:mm) : ')
        fecha_object = datetime.strptime(fecha, '%d-%m-%Y %H:%M')
        self.clinica.agendar_turno(dni,matricula,especialidad,fecha_object)
        turno = self.clinica.obtener_turnos()[-1]
        print('turno agendado con exito!!')    
        print(turno)
    
    def agregar_especialidad(self):
        nombre:str = input('Ingrese el nombre de la especialidad: ')
        matricula:str = input('Ingrese la matricula del medico: ')
        medico:Medico = self.clinica.obtener_medico_por_matricula(matricula)
        ele:bool = True
        dias:list[str] =[]
        while ele:
            dia = input('Ingrese el dia para esa especialidad (para dejar de elejir, escriba 0) ')
            if dia =='0':
                ele=False
            else:   
                dias.append(dia)
        especialidad = Especialidad(nombre,dias)
        medico.agregar_especialidad(especialidad)
        print('Especialidad ingresada con exito !!')
    
    def emitir_receta(self):
        dni = input('Ingrese el DNI del paciente: ')
        matricula = input('Ingrese la matricula del medico: ')
        ele:bool = True
        medicamentos:list[str] =[]
        while ele:
            med = input('Ingrese los medicamentos para esta receta (para dejar de elejir, escriba 0): ')
            if med =='0':
                ele=False
            else:
                medicamentos.append(med)
        self.clinica.emitir_receta(dni,matricula,medicamentos)
        print('Receta emitida con exito!!')
    def ver_historia_clinica(self):
        dni = input('ingrese dni del paciente ')
        print(self.clinica.obtener_historia_clinica(dni))
    
    def ver_turnos(self):
        turnos = self.clinica.obtener_turnos()
        print('--TURNOS--')
        for i, t in enumerate(turnos):
            print(f'{i+1}- {t}')
    
    def ver_pacientes(self):
        pacientes = self.clinica.obtener_pacientes()
        print('--PACIENTES--')
        for i, p in enumerate(pacientes):
            print(f'{i+1}- {p}')
    
    def ver_medicos(self):
        medicos = self.clinica.obtener_medicos()
        print('--MEDICOS--')
        for i, m in enumerate(medicos):
            print(f'{i+1}- {m}')

if __name__ == '__main__':

    menu_clinica = CLI()
    eligiendo = True
    print('''
    --- Menú Clínica ---
    1) Agregar paciente\n
    2) Agregar médico\n
    3) Agendar turno\n
    4) Agregar especialidad\n
    5) Emitir receta\n
    6) Ver historia clínica\n
    7) Ver todos los turnos\n
    8) Ver todos los pacientes\n
    9) Ver todos los médicos\n
    0) Salir\n
    ''')
    while eligiendo:
        seleccion = int(input('¿Que quiere hacer? '))
        match seleccion:
            case 0:
                eligiendo = False
            case 1:
                try:
                    menu_clinica.agregar_paciente()
                except ValueError as v:
                    print(v)
            case 2:
                try:
                   menu_clinica.agregar_medico()
                except ValueError as v:
                    print(v)
            case 3:
                try:
                    menu_clinica.agendar_turno()
                except MedicoNoDisponibleException as med:
                    print(med)
                except PacienteNoEncontradoException as p_no_encontrado:
                    print(p_no_encontrado)
                except TurnoOcupadoException as to:
                    print(TurnoOcupadoException)
            case 4:
                try:
                    menu_clinica.agregar_especialidad()
                except MedicoNoDisponibleException as mnd:
                    print(mnd)
                except ValueError as v:
                    print(v)
            case 5:
                try:
                    menu_clinica.emitir_receta()
                except RecetaInvalidaException as ri:
                    print(ri)
                except PacienteNoEncontradoException as p_no_encontrado:
                    print(p_no_encontrado)
                except MedicoNoDisponibleException as mnd:
                    print(mnd)
            case 6:
                try:
                    menu_clinica.ver_historia_clinica()
                except PacienteNoEncontradoException as pn:
                    print(pn)

            case 7:
                menu_clinica.ver_turnos()
            case 8:
                menu_clinica.ver_pacientes()
            case 9:
                menu_clinica.ver_medicos()
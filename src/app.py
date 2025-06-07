from models.Clinica import Clinica
from models.Paciente import Paciente
from models.Medico import Medico
from models.Turno import Turno
from models.Receta import Receta
from datetime import datetime
from models.Especialidad import Especialidad
from exceptions.MedicoNoDisponibleException import MedicoNoDisponibleException
from exceptions.PacienteNoEncontradoException import PacienteNoEncontradoException
from exceptions.RecetaInvalidaException import RecetaInvalidaException
from exceptions.TurnoOcupadoException import TurnoOcupadoException



clinica = Clinica()

def agregar_paciente():
    nombre = input('Ingrese el nombre del paciente: ')
    dni = input('Ingrese el dni del paciente: ')
    nacimiento = input('Ingrese la fecha de nacimiento del paciente: ')
    paciente = Paciente(nombre,dni,nacimiento)
    clinica.agregar_paciente(paciente)
    print('Paciente agregado con exito!!')
    print(paciente)

def agregar_medico():
    nombre = input('Ingrese el nombre del medico: ')
    matricula = input('Ingrese la matricula del medico: ')
    medico = Medico(nombre,matricula)
    clinica.agregar_medico(medico)
    print('Medico agregado con exito!!')
    print(medico)

def agendar_turno():
    dni = input('Ingrese dni del paciente: ')
    matricula = input('Ingrese la matricula del medico: ')
    especialidad = input('Ingrese la especialidad del medico: ')
    fecha = input('Ingrese la fecha y hora (dd-mm-yyyy hh:mm) : ')
    fecha_object = datetime.strptime(fecha, '%d-%m-%Y %H:%M')
    clinica.agendar_turno(dni,matricula,especialidad,fecha_object)
    turno = clinica.obtener_turnos()[-1]
    # paciente = clinica.obtener_paciente_por_dni(dni)
    # medico = clinica.obtener_medico_por_matricula(matricula)
    print('turno agendado con exito!!')    
    print(turno)

def agregar_especialidad():
    nombre:str = input('Ingrese el nombre de la especialidad')
    matricula:str = input('Ingrese la matricula del medico')
    medico:Medico = clinica.obtener_medico_por_matricula(matricula)
    ele:bool = True
    dias:list[str] =[]
    while ele:
        dia = input('Ingrese el dia para esa especialidad (para dejar de elejir, escriba 0)')
        if dia =='0':
            ele=False
        dias.append(dia)

    especialidad = Especialidad(nombre,dias)
    medico.agregar_especialidad(especialidad)
    print('Especialidad ingresada con exito !!')

def emitir_receta():
    dni = input('Ingrese el DNI del paciente')
    matricula = input('Ingrese la matricula del medico')
    ele:bool = True
    medicamentos:list[str] =[]
    while ele:
        med = input('Ingrese los medicamentos para esta receta (para dejar de elejir, escriba 0)')
        if med =='0':
            ele=False
        medicamentos.append(med)
    clinica.emitir_receta(dni,matricula,medicamentos)
    print('Receta emitida con exito!!')
def ver_historia_clinica():
    dni = input('ingrese dni del paciente')
    print(clinica.obtener_historia_clinica(dni))

def ver_turnos():
    turnos = clinica.obtener_turnos()
    print('--TURNOS--')
    for i, t in enumerate(turnos):
        print(f'{i+1}- {t}')

def ver_pacientes():
    pacientes = clinica.obtener_pacientes()
    print('--PACIENTES--')
    for i, p in enumerate(pacientes):
        print(f'{i+1}- {p}')

def ver_medicos():
    medicos = clinica.obtener_medicos()
    print('--MEDICOS--')
    for i, m in enumerate(medicos):
        print(f'{i+1}- {m}')

if __name__ == '__main__':
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
        seleccion = int(input('¿Que quiere hacer?'))
        match seleccion:
            case 0:
                eligiendo = False
            case 1:
                agregar_paciente()
            case 2:
                agregar_medico()
            case 3:
                try:
                    agendar_turno()
                except MedicoNoDisponibleException:
                    print('El medico no esta disponible')
                except PacienteNoEncontradoException:
                    print('El paciente no fue encontrado')
            case 4:
                agregar_especialidad()
            case 5:
                emitir_receta()
            case 6:
                try:
                    ver_historia_clinica()
                except PacienteNoEncontradoException:
                    print('paciente no encontrado')
            case 7:
                ver_turnos()
            case 8:
                ver_pacientes()
            case 9:
                ver_medicos()
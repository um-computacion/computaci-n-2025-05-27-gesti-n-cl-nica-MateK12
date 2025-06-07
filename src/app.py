from models.Paciente import Paciente
from models.Especialidad import Especialidad
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
        if seleccion==0:
            eligiendo = False
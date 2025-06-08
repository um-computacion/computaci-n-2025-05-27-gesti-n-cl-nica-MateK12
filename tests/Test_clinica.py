import unittest
from src.models.Paciente import Paciente
from src.models.Clinica import Clinica
from src.models.HistoriaClinica import HistoriaClinica
from src.models.Medico import Medico
from src.models.Especialidad import Especialidad
from src.models.HistoriaClinica import HistoriaClinica
from datetime import datetime, timedelta
from src.exceptions.MedicoNoDisponibleException import MedicoNoDisponibleException
from src.exceptions.PacienteNoEncontradoException import PacienteNoEncontradoException
from src.exceptions.RecetaInvalidaException import RecetaInvalidaException
from src.exceptions.TurnoOcupadoException import TurnoOcupadoException
class Test_clinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Juan Pérez", "12345678", "1990-01-01")
        self.medico = Medico("Dra. Gómez", "A123")
        self.especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)
        self.fecha_turno = datetime(2025, 6, 23, 10, 0)  
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
    
    def test_agregar_paciente(self):
        dni='83838'
        paciente = Paciente('Mateo',dni,'24-03-2003')
        self.clinica.agregar_paciente(paciente)
        self.assertEqual(self.clinica.obtener_pacientes()[-1],paciente)
        self.assertIsInstance(self.clinica.obtener_historia_clinica(dni),HistoriaClinica)

    def test_agregar_paciente_dni_repetido(self):
        with self.assertRaises(ValueError):
            paciente = Paciente('mateo','83838','24-03-2003')
            self.clinica.agregar_paciente(paciente)
            self.clinica.agregar_paciente(paciente)

    


    def test_agregar_especialidad_nueva_a_medico(self):
        nueva_especialidad = Especialidad("Dermatología", ["viernes"])
        self.medico.agregar_especialidad(nueva_especialidad)
        self.assertEqual(
            self.medico.obtener_especialidad_para_dia("viernes"), "Dermatología"
        )

    def test_no_permitir_especialidades_duplicadas(self):
        with self.assertRaises(ValueError):
            self.medico.agregar_especialidad(self.especialidad)


    def test_especialidad_con_dias_invalidos(self):
        especialidad_invalida = Especialidad("Gastro", ["abcd"])
        self.medico.agregar_especialidad(especialidad_invalida)
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("viernes"))

    def test_error_agregar_especialidad_a_medico_no_existente(self):
        clinica = Clinica()
        with self.assertRaises(MedicoNoDisponibleException):
            clinica.obtener_medico_por_matricula("XXXX")


    def test_agendamiento_turno_correcto(self):
        self.clinica.agendar_turno("12345678", "A123", "Cardiología", self.fecha_turno)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)

    def test_turno_duplicado(self):
        self.clinica.agendar_turno("12345678", "A123", "Cardiología", self.fecha_turno)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("12345678", "A123", "Cardiología", self.fecha_turno)

    def test_turno_paciente_no_existente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "A123", "Cardiología", self.fecha_turno)

    def test_turno_medico_no_existente(self):
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "X999", "Cardiología", self.fecha_turno)

    def test_turno_especialidad_invalida(self):
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "A123", "Pediatría", self.fecha_turno)

    def test_turno_en_dia_no_laboral(self):
        
        fecha_martes = self.fecha_turno = datetime(2025, 6, 24, 10, 0)  
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "A123", "Cardiología", fecha_martes)


    def test_emitir_receta_correctamente(self):
        medicamentos = ["Paracetamol", "Ibuprofeno"]
        self.clinica.emitir_receta("12345678", "A123", medicamentos)
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_paciente_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "A123", ["Paracetamol"])

    def test_emitir_receta_medico_inexistente(self):
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.emitir_receta("12345678", "Z999", ["Paracetamol"])

    def test_emitir_receta_sin_medicamentos(self):
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "A123", [])


    def test_historia_clinica_turno_y_receta_guardados(self):
        self.clinica.agendar_turno("12345678", "A123", "Cardiología", self.fecha_turno)
        self.clinica.emitir_receta("12345678", "A123", ["Ibupirac"])
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)





if __name__=="__main__":
    unittest.main()
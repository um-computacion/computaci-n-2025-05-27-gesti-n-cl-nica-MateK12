import unittest
from src.models.Paciente import Paciente
from src.models.Clinica import Clinica
from src.models.HistoriaClinica import HistoriaClinica
from src.models.Medico import Medico
from src.models.Especialidad import Especialidad
from src.models.HistoriaClinica import HistoriaClinica
from src.models.Turno import Turno
from src.models.Receta import Receta

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

class TestEspecialidad(unittest.TestCase):

    def setUp(self):
        self.especialidad = Especialidad("Cardiología", ["Lunes", "Miércoles", "Viernes"])

    def test_obtener_especialidad(self):
        self.assertEqual(self.especialidad.obtener_especialidad(), "Cardiología")

    def test_verificar_dia_presente(self):
        self.assertTrue(self.especialidad.verificar_dia("Lunes"))

    def test_verificar_dia_mayusculas(self):
        self.assertTrue(self.especialidad.verificar_dia("VIERNES"))

    def test_verificar_dia_ausente(self):
        self.assertFalse(self.especialidad.verificar_dia("Martes"))

    def test_verificar_dia_con_minusculas(self):
        self.assertTrue(self.especialidad.verificar_dia("miércoles"))

    def test_str_output(self):
        esperado = "Especialidad: Cardiología dias Lunes, Miércoles, Viernes"
        self.assertEqual(str(self.especialidad), esperado)

    def test_dia_lista_vacía(self):
        esp = Especialidad("Dermatología", [])
        self.assertFalse(esp.verificar_dia("Lunes"))

    def test_tipo_vacio(self):
        esp = Especialidad("", ["Lunes"])
        self.assertEqual(esp.obtener_especialidad(), "")

    def test_dias_con_acentos(self):
        esp = Especialidad("Pediatría", ["Miércoles", "Jueves"])
        self.assertTrue(esp.verificar_dia("miércoles"))
class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Laura Méndez", "44556677", "1978-03-22")
        self.historia = HistoriaClinica(self.paciente)

        self.medico = Medico("Dr. Peña", "M123")
        self.turno = Turno(self.paciente, self.medico, "2024-10-10 15:00", "cardiologia")
        self.receta = Receta(self.paciente, ["Paracetamol"], self.medico)


    def test_agregar_turno(self):
        self.historia.agregar_turno(self.turno)
        self.assertEqual(len(self.historia.obtener_turnos()), 1)

    def test_agregar_varios_turnos(self):
        self.historia.agregar_turno(self.turno)
        self.historia.agregar_turno(self.turno)
        self.assertEqual(len(self.historia.obtener_turnos()), 2)

    def test_agregar_receta(self):
        self.historia.agregar_receta(self.receta)
        self.assertEqual(len(self.historia.obtener_recetas()), 1)

    def test_str_contiene_datos_paciente(self):
        texto = str(self.historia)
        self.assertIn("Laura Méndez", texto)
        self.assertIn("44556677", texto)

    def test_str_sin_turnos_muestra_mensaje(self):
        texto = str(self.historia)
        self.assertIn("No hay turnos registrados", texto)


class TestMedico(unittest.TestCase):

    def setUp(self):
        self.medico = Medico("Adolfo", "12345")
        self.esp1 = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        self.esp2 = Especialidad("Neurología", ["Martes"])
        self.medico.agregar_especialidad(self.esp1)
        self.medico.agregar_especialidad(self.esp2)

    def test_obtener_matricula(self):
        self.assertEqual(self.medico.obtener_matricula(), "12345")

    def test_agregar_especialidad(self):
        dia="Viernes"
        esp = Especialidad("Dermatología", [dia])
        self.medico.agregar_especialidad(esp)
        self.assertEqual("Dermatología", self.medico.obtener_especialidad_para_dia(dia))

    def test_obtener_especialidad_para_dia_existente(self):
        self.assertEqual(self.medico.obtener_especialidad_para_dia("Lunes"), "Cardiología")

    def test_obtener_especialidad_para_dia_existente_2(self):
        self.assertEqual(self.medico.obtener_especialidad_para_dia("Martes"), "Neurología")

    def test_obtener_especialidad_para_dia_inexistente(self):
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("Domingo"))

    def test_obtener_especialidad_para_dia_case_insensitive(self):
        self.assertEqual(self.medico.obtener_especialidad_para_dia("miércoles"), "Cardiología")

    def test_str_output(self):
        resultado = str(self.medico)
        self.assertIn("Adolfo", resultado)
        self.assertIn("12345", resultado)
        self.assertIn("Cardiología", resultado)
        self.assertIn("Neurología", resultado)

    def test_sin_especialidades(self):
        medico_vacio = Medico("Dra. Gómez", "67890")
        self.assertIsNone(medico_vacio.obtener_especialidad_para_dia("Lunes"))
        self.assertEqual(str(medico_vacio), "Nombre:Dra. Gómez, matricula: 67890 especialidades: ")

    def test_multiple_especialidades_mismo_dia(self):
        esp3 = Especialidad("Pediatría", ["Lunes"])
        self.medico.agregar_especialidad(esp3)
        self.assertEqual(self.medico.obtener_especialidad_para_dia("Lunes"), "Cardiología")
class TestPaciente(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Mateo Gómez", "12345678", "24-02-2025")

    def test_obtener_dni(self):
        self.assertEqual(self.paciente.obtener_dni(), "12345678")

    def test_str_contiene_nombre(self):
        resultado = str(self.paciente)
        self.assertIn("Mateo Gómez", resultado)

    def test_str_contiene_dni(self):
        resultado = str(self.paciente)
        self.assertIn("12345678", resultado)

    def test_str_contiene_fecha_nacimiento(self):
        resultado = str(self.paciente)
        self.assertIn("24-02-2025", resultado)


    def test_paciente_con_nombre_vacio(self):
        paciente = Paciente("", "98765432", "2000-01-01")
        self.assertIn("Paciente: ", str(paciente))


    def test_str_output_completo(self):
        esperado = "Paciente: Mateo Gómez | DNI: 12345678 | Fecha de Nacimiento: 24-02-2025"
        self.assertEqual(str(self.paciente), esperado)

class TestReceta(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Juan Pérez", "12345678",'24-02-2025')
        self.medico = Medico("Dra. Sánchez", "M001")
        self.medicamentos = ["Ibuprofeno", "Paracetamol"]
        self.receta = Receta(self.paciente, self.medicamentos, self.medico)



    def test_str_contiene_paciente(self):
        self.assertIn("Juan Pérez", str(self.receta))

    def test_str_contiene_medico(self):
        self.assertIn("Dra. Sánchez", str(self.receta))

    def test_str_contiene_medicamentos(self):
        self.assertIn("Ibuprofeno", str(self.receta))
        self.assertIn("Paracetamol", str(self.receta))

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Julián Torres", "12345678", "1992-06-01")
        self.medico = Medico("Dra. Suárez", "M456")
        self.fecha = datetime(2025, 7, 15, 10, 30)
        self.turno = Turno(self.paciente, self.medico, self.fecha, "Cardiología")

    def test_obtener_medico(self):
        medico = self.turno.obtener_medico()
        self.assertEqual(medico.obtener_matricula(), "M456")

    def test_obtener_fecha_hora(self):
        fecha = self.turno.obtener_fecha_hora()
        self.assertEqual(fecha, self.fecha)

    def test_str_contiene_nombre_paciente(self):
        resultado = str(self.turno)
        self.assertIn("Julián Torres", resultado)

    def test_str_contiene_nombre_medico(self):
        resultado = str(self.turno)
        self.assertIn("Dra. Suárez", resultado)


    def test_str_formato_general(self):
        resultado = str(self.turno)
        self.assertTrue(resultado.startswith("Paciente:"))

if __name__=="__main__":
    unittest.main()
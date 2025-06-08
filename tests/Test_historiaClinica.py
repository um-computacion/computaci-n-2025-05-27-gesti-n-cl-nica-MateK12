import unittest
from src.models.HistoriaClinica import HistoriaClinica
from src.models.Paciente import Paciente
from src.models.Turno import Turno
from src.models.Receta import Receta
from src.models.Medico import Medico

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


if __name__ == "__main__":
    unittest.main()

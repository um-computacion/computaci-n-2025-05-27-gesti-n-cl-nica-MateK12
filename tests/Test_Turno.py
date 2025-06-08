import unittest
from datetime import datetime
from src.models.Turno import Turno
from src.models.Medico import Medico
from src.models.Paciente import Paciente

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


if __name__ == "__main__":
    unittest.main()

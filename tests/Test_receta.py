import unittest
from datetime import datetime
from src.models.Receta import Receta
from src.models.Medico import Medico
from src.models.Paciente import Paciente

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


if __name__ == "__main__":
    unittest.main()

import unittest
from src.models.Paciente import Paciente

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

if __name__ == "__main__":
    unittest.main()

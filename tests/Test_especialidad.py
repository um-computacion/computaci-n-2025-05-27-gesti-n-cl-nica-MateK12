import unittest
from src.models.Especialidad import Especialidad
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



if __name__ == "__main__":
    unittest.main()

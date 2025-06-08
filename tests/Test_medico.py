import unittest
from src.models.Especialidad import Especialidad
from src.models.Medico import Medico  

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



if __name__ == "__main__":
    unittest.main()

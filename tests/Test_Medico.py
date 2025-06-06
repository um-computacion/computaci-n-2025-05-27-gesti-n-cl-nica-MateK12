from src.models.Especialidad import Especialidad
from src.models.Medico import Medico
import unittest
from unittest.mock import patch
import io
import sys
class TestMedico(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.medico = Medico("Dr. Juan Pérez", "MAT12345")
        self.cardiologia = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        self.pediatria = Especialidad("Pediatría", ["Martes", "Jueves"])
        self.neurologia = Especialidad("Neurología", ["Viernes"])
    
    def test_init(self):
        """Test del constructor"""
        self.assertEqual(self.medico.obtener_matricula(), "MAT12345")
    
    def test_obtener_matricula(self):
        """Test del método obtener_matricula"""
        medico2 = Medico("Dra. Ana García", "MAT54321")
        self.assertEqual(self.medico.obtener_matricula(), "MAT12345")
        self.assertEqual(medico2.obtener_matricula(), "MAT54321")
    
    def test_agregar_especialidad_una(self):
        """Test agregar una especialidad"""
        self.medico.agregar_especialidad(self.cardiologia)

        with patch('sys.stdout', new_callable=io.StringIO):
            resultado = self.medico.obtener_especialidad_para_dia("lunes")
        self.assertEqual(resultado, "Cardiología")
    
    def test_agregar_especialidad_multiples(self):
        """Test agregar múltiples especialidades"""
        self.medico.agregar_especialidad(self.cardiologia)
        self.medico.agregar_especialidad(self.pediatria)
        
        with patch('sys.stdout', new_callable=io.StringIO):
            resultado_lunes = self.medico.obtener_especialidad_para_dia("lunes")
            resultado_martes = self.medico.obtener_especialidad_para_dia("martes")
        
        self.assertEqual(resultado_lunes, "Cardiología")
        self.assertEqual(resultado_martes, "Pediatría")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_obtener_especialidad_para_dia_existente(self, mock_stdout):
        """Test obtener especialidad para día existente"""
        self.medico.agregar_especialidad(self.cardiologia)
        resultado = self.medico.obtener_especialidad_para_dia("miércoles")
        self.assertEqual(resultado, "Cardiología")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_obtener_especialidad_para_dia_no_existente(self, mock_stdout):
        """Test obtener especialidad para día no existente"""
        self.medico.agregar_especialidad(self.cardiologia)
        resultado = self.medico.obtener_especialidad_para_dia("domingo")
        self.assertIsNone(resultado)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_obtener_especialidad_para_dia_sin_especialidades(self, mock_stdout):
        """Test obtener especialidad cuando el médico no tiene especialidades"""
        resultado = self.medico.obtener_especialidad_para_dia("lunes")
        self.assertIsNone(resultado)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_obtener_especialidad_para_dia_primera_coincidencia(self, mock_stdout):
        """Test que devuelve la primera especialidad que coincide"""
        especialidad1 = Especialidad("Primera", ["Lunes"])
        especialidad2 = Especialidad("Segunda", ["Lunes"])
        
        self.medico.agregar_especialidad(especialidad1)
        self.medico.agregar_especialidad(especialidad2)
        
        resultado = self.medico.obtener_especialidad_para_dia("lunes")
        self.assertEqual(resultado, "Primera") 
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_obtener_especialidad_para_dia_case_insensitive(self, mock_stdout):
        """Test que la búsqueda es case insensitive"""
        self.medico.agregar_especialidad(self.cardiologia)
        resultado = self.medico.obtener_especialidad_para_dia("LUNES")
        self.assertEqual(resultado, "Cardiología")
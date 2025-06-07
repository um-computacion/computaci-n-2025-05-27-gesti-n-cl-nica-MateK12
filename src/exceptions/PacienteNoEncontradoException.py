class PacienteNoEncontradoException(Exception):

    def __init__(self, mensaje="Paciente no encontrado en el sistema"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
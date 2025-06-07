class MedicoNoDisponibleException(Exception):

    def __init__(self, mensaje="Médico no disponible para la fecha y hora solicitada"):

        self.mensaje = mensaje
        super().__init__(self.mensaje)
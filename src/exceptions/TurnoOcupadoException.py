class TurnoOcupadoException(Exception):
    def __init__(self, mensaje="El turno solicitado ya está ocupado"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

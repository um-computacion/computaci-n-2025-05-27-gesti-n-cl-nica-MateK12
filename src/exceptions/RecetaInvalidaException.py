class RecetaInvalidaException(Exception):

    def __init__(self, mensaje="La receta médica no es válida"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
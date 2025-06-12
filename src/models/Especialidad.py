class Especialidad():
    def __init__(self,tipo:str,dias:list[str]):
        self.__tipo__= tipo
        self.__dias__= dias
    def obtener_especialidad(self) -> str:
        return self.__tipo__
    def obtener_dias(self) -> list[str]:
        return self.__dias__
    def verificar_dia(self,dia:str)-> bool:
        dia = dia.lower()
        arr = [ d.lower() for d in  self.__dias__ ]
        if dia in arr:
            return True
        else:
            return False
    def __str__(self):
        return f"Especialidad: {self.__tipo__} dias {', '.join(self.__dias__)}"
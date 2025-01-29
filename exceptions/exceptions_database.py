class UniqueViolationError(Exception):
    """Excepción para manejo de violación de clave única."""
    pass

class NotValidCapacity(Exception):
    def __init__(self, message="La capacidad no es valida para el torneo"):
        self.message = message
        super().__init__(self.message)

class FutureDateNotAllowedError(Exception):
    def __init__(self, message="La fecha de inicio es superior a la fecha de finalización"):
        self.message = message
        super().__init__(self.message)

class StatusNotAllowed(Exception):
    def __init__(self, message="El estado que quieres ingresar no esta permitido"):
        self.message = message
        super().__init__(self.message)
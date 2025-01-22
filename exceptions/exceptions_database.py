import mysql.connector

class UniqueViolationError(Exception):
    """Excepción para manejo de violación de clave única."""
    pass
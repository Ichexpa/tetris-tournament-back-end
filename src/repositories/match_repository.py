from src.models.tournament import Tournament
from mysql.connector.errors import IntegrityError
from src.exceptions.exceptions_database import UniqueViolationError

class MatchRepository():

    def __init__(self,db):
        self.db = db

    
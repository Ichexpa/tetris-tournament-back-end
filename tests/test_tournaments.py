import pytest
from config import TestingConfig
from src.db import Database
from src.models.tournament import Tournament
from src.repositories.tournament_repository import TournamentRepository
from tests.utils import cleanup
from mysql.connector.errors import IntegrityError, DataError
from exceptions.exceptions_database import NotValidCapacity,FutureDateNotAllowedError

@pytest.fixture
def config():
    db = Database(TestingConfig)
    return db


@pytest.fixture
def tournament_repository(config):
    db = config
    return TournamentRepository(db)


@pytest.fixture(autouse=True)
def setup(config):
    db = config

    with db.get_connection() as conn:
        cursor = conn.cursor()

        with open("tetris_tournament_data_test.sql", "r") as file:
            sql_script = file.read()

        sql_statements = sql_script.split(";")

        for statement in sql_statements:
            if statement.strip():
                cursor.execute(statement)

        conn.commit()

        cursor.close()

    yield

    db = config
    with db.get_connection() as conn:
        cleanup(conn)

def test_save_with_all_fields(tournament_repository):
    # Arrange
    """El metodo save de TournamentRepository recibe un Tournament que recibe en el campo organizer_id
    un user_id ya que en el procedimiento almacenado, hace la busqueda del organizer_id en base al user_id
    para colocarlo en el campo correspondiente, es por eso que paso organizer_id=8 en lugar
    de 1 o 2 que son los que estan cargados en "tetris_tournament_data_test.sql"  """
    
    tournament = Tournament(
        name="Tetris Royale",
        capacity=8,
        total_points=100,
        organizer_id=8,
        status="Activo",
        start_date="2025-02-10",
        end_date = "2025-02-20",
        best_of=3
    )

    # Act
    saved_tournament = tournament_repository.save(tournament)
    # Assert
    assert saved_tournament.id == 3

def test_save_with_incorrect_id(tournament_repository):
    # Arrange
    id_erroneo= 666
    tournament = Tournament(
        name= "Tetris Racing",
        capacity= 8,
        total_points= 100,
        organizer_id= id_erroneo,
        start_date= "2025-02-10",
        end_date = "2025-02-20"
    )

    # Act
    # Assert
    with pytest.raises(IntegrityError):
        tournament_repository.save(tournament)


def test_save_with_incorrect_capacity(tournament_repository):
    # Arrange
    capacidad_incorrecta = 33
    tournament = Tournament(
        name= "Tetris Champions",
        capacity= capacidad_incorrecta,
        total_points= 100,
        organizer_id= 8,
        start_date= "2025-02-10",
        end_date = "2025-02-20"
    )
    # Act
    # Assert
    with pytest.raises(NotValidCapacity):
        tournament_repository.save(tournament)

def test_save_with_bad_date(tournament_repository):
    # Arrange
    fecha_incio = "2025-02-25"
    fecha_final = "2025-02-24"
    tournament = Tournament(
        name= "Tetris GOTY",
        capacity= 8,
        total_points= 100,
        organizer_id= 8,
        start_date= fecha_incio,
        end_date = fecha_final
    )
    # Act
    # Assert
    with pytest.raises(FutureDateNotAllowedError):
        tournament_repository.save(tournament)


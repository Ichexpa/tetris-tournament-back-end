import pytest
from config import TestingConfig
from src.db import Database
from src.models.tournament import Tournament
from src.repositories.tournament_repository import TournamentRepository
from tests.utils import cleanup
from mysql.connector.errors import IntegrityError
from exceptions.exceptions_database import NotValidCapacity,FutureDateNotAllowedError,StatusNotAllowed
from datetime import datetime

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

##SUT :update

def test_update_all_fields_success(tournament_repository):
    # Arrange
    tournament = Tournament(
        id=1,
        name="Torneo modificado",
        capacity= 16,
        total_points= 500,
        status="En curso",
        organizer_id=2,        
        start_date= "2025-02-15",
        end_date = "2025-02-25",
        best_of = 3
    )

    # Act
    tournament_repository.update(tournament)
    updated_tournament = tournament_repository.get_tournament_by_id(Tournament(id=1))
    # Assert    
    assert updated_tournament.name == "Torneo modificado"
    assert updated_tournament.capacity == 16
    assert updated_tournament.total_points == 500
    assert updated_tournament.status == "En curso"
    assert updated_tournament.start_date == datetime.strptime("2025-02-15", "%Y-%m-%d").date() 
    assert updated_tournament.end_date == datetime.strptime("2025-02-25", "%Y-%m-%d").date()
    assert updated_tournament.organizer_id == 2
    

def test_update_partial_fields(tournament_repository):
    # Arrange
    original_tournament = tournament_repository.get_tournament_by_id(Tournament(id=1))
    tournament = Tournament(
        id=1,
        name="Actualización parcial",
        status = "En curso",
        total_points = 450
    )
    # Act
    tournament_repository.update(tournament)
    updated_tournament = tournament_repository.get_tournament_by_id(Tournament(id=1))

    # Assert
    assert updated_tournament.name == "Actualización parcial"
    assert updated_tournament.capacity == original_tournament.capacity
    assert updated_tournament.total_points == 450
    assert updated_tournament.status == "En curso"
    assert updated_tournament.start_date == original_tournament.start_date
    assert updated_tournament.end_date == original_tournament.end_date
    assert updated_tournament.organizer_id == original_tournament.organizer_id

def test_update_with_invalid_status(tournament_repository):
  # Arrange
    original_tournament = tournament_repository.get_tournament_by_id(Tournament(id=1))
    tournament = Tournament(
        id=1,
        status = "Estado no existente"
    )

    # Act & Assert
    with pytest.raises(StatusNotAllowed):
        tournament_repository.update(tournament)
        
    #Assert
    current_tournament = tournament_repository.get_tournament_by_id(Tournament(id=1))
    assert current_tournament.status == original_tournament.status
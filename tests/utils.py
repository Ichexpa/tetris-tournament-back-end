def cleanup(conn):
    """Fixture para limpiar la base de datos y resetear ids."""
    with conn.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # Reset table users
        cursor.execute("TRUNCATE TABLE users;")
        cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1;")
        # Reset table players
        cursor.execute("TRUNCATE TABLE players;")
        cursor.execute("ALTER TABLE players AUTO_INCREMENT = 1;")
        # Reset table organizers
        cursor.execute("TRUNCATE TABLE organizers;")
        cursor.execute("ALTER TABLE organizers AUTO_INCREMENT = 1;")
        # Reset table tournaments
        cursor.execute("TRUNCATE TABLE tournaments;")
        cursor.execute("ALTER TABLE tournaments AUTO_INCREMENT = 1;")
        # Reset table tournamentsxplayers
        cursor.execute("TRUNCATE TABLE tournamentsxplayers;")
        cursor.execute("ALTER TABLE tournamentsxplayers AUTO_INCREMENT = 1;")

        conn.commit()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
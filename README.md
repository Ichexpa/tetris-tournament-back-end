# Sistema Gestor de Torneos de Tetris

Pablo Ramírez, presidente de la Asociación de eSports del Centro Cultural Digital, se
 comunicó con el equipo de desarrollo para solicitar el diseño de un sistema que permita
 gestionar los torneos de Tetris que organizan mensualmente. Pablo plantea la siguiente
 situación.
 Actualmente, los organizadores del centro cultural gestionan los torneos de manera manual
 utilizando hojas de cálculo y grupos de mensajería, lo que dificulta el seguimiento de las
 partidas y la coordinación entre participantes.
 En base a esto, se busca crear un sistema donde tanto organizadores como jugadores
 puedan registrarse para participar de manera organizada.
 Los organizadores deben poder crear torneos especificando nombre, fechas de inicio y fin,
 cantidad máxima de participantes y reglas básicas del formato (mejor de 3 o mejor de 5
 partidas). Los torneos pueden configurarse en formato de eliminación simple o doble
 (opcional) según se desee.
 Para participar, los jugadores deben poder inscribirse en los torneos disponibles y
 confirmar su participación antes del inicio. El sistema debe mostrar claramente la lista de
 participantes y el estado de sus confirmaciones. Una vez alcanzado el máximo de
 participantes, las inscripciones deben cerrarse automáticamente.
 Una vez iniciado el torneo, el sistema debe generar automáticamente las llaves iniciales y
 mostrar el bracket actualizado. Los organizadores serán los responsables de registrar los
 resultados de cada partida, tras lo cual el bracket debe actualizarse automáticamente.
 Cada jugador debe tener un perfil que muestre sus estadísticas básicas (victorias/derrotas)
 y su historial de participación en torneos anteriores. El sistema debe mantener un ranking
 global que refleje el desempeño de los jugadores. Los puntos se otorgarán según la
 posición final obtenida en cada torneo, con bonificaciones por participar en torneos más
 grandes y un sistema de decaimiento para torneos antiguos. Esto asegura que el ranking
 refleje tanto el rendimiento histórico como la actividad reciente de los jugadores.
 Tanto organizadores como jugadores deben tener acceso a un panel personalizado donde
 pueden ver los torneos activos y sus próximos enfrentamientos. Los torneos deben poder
 filtrarse por estado (próximo, en curso, finalizado), nombre y fecha para facilitar su
 búsqueda.

## Objetivo

En este proyecto se implementará una API RESTful con Python y Flask, la cual permitirá gestionar la organización de los torneos y facilitar la inscripción de los jugadores a estos, registrando sus resultados y ranking . Se implementará una capa de autenticación para los usuarios mediante JWT.

## Estructura del proyecto

```bash
gespro/
│   src/
│   ├── db.py
│   ├── models/
│   │   ├── user_model.py
│   ├── repositories/
│   │   ├── user_repository.py
│   ├── exceptions/
│   │   ├── custom_exceptions.py
│   ├── services/
│   │   ├── user_service.py
│   ├── controllers/
│   │   ├── user_controller.py
│   ├── utils/
├── tests/
│   app.py
│   config.py
```

## Requerimientos

- Python 3.10+
- Flask 3.1.0
- MySQL Connector 9.1
- Flask JWT Extended 4.7.1
- bcrypt 4.2.1
- Flask Cors 5.0.0
- Python Dotenv 1.0.1
- Pytest

## Instalación

1. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

2. Crear un archivo `.env` en la raíz del proyecto. El repositorio cuenta con un archivo `.env.example` que puedes utilizar como base.

3. Crear una base de datos en MySQL y configurar las credenciales en el archivo `.env`.

4. Para lanzar la aplicación, ejecutar el siguiente comando:

```bash
flask --app app run
```
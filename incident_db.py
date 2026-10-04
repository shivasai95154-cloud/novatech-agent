import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DATABASE_FILE = Path(__file__).parent / "novatech.db"


def get_connection():
    """
    Create a connection to the NovaTech SQLite database.
    """

    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    """
    Create the incidents table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_number TEXT UNIQUE,
            system_name TEXT NOT NULL,
            detected_status TEXT NOT NULL,
            response_time_ms INTEGER,
            incident_status TEXT NOT NULL,
            detected_at TEXT NOT NULL,
            resolved_at TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def get_open_incident(system_name):
    """
    Return the existing OPEN incident for a system,
    if one exists.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            incident_number,
            system_name,
            detected_status,
            response_time_ms,
            incident_status,
            detected_at,
            resolved_at
        FROM incidents
        WHERE system_name = ?
        AND incident_status = 'OPEN'
        ORDER BY id DESC
        LIMIT 1
        """,
        (system_name,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "incident_number": row[0],
        "system": row[1],
        "detected_status": row[2],
        "response_time_ms": row[3],
        "incident_status": row[4],
        "detected_at": row[5],
        "resolved_at": row[6]
    }


def create_incident(incident):
    """
    Create a new incident only when the affected system
    does not already have an OPEN incident.
    """

    existing_incident = get_open_incident(
        incident["system"]
    )

    if existing_incident:
        return existing_incident, False

    connection = get_connection()

    cursor = connection.cursor()

    detected_at = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute(
        """
        INSERT INTO incidents (
            incident_number,
            system_name,
            detected_status,
            response_time_ms,
            incident_status,
            detected_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "TEMP",
            incident["system"],
            incident["status"],
            incident["response_time_ms"],
            "OPEN",
            detected_at
        )
    )

    database_id = cursor.lastrowid

    incident_number = (
        f"INC-{database_id:04d}"
    )

    cursor.execute(
        """
        UPDATE incidents
        SET incident_number = ?
        WHERE id = ?
        """,
        (
            incident_number,
            database_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "incident_number": incident_number,
        "system": incident["system"],
        "detected_status": incident["status"],
        "response_time_ms": incident[
            "response_time_ms"
        ],
        "incident_status": "OPEN",
        "detected_at": detected_at,
        "resolved_at": None
    }, True


def resolve_incident(system_name):
    """
    Resolve an existing OPEN incident for a system.
    """

    existing_incident = get_open_incident(
        system_name
    )

    if not existing_incident:
        return None, False

    resolved_at = datetime.now(
        timezone.utc
    ).isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE incidents
        SET incident_status = 'RESOLVED',
            resolved_at = ?
        WHERE incident_number = ?
        """,
        (
            resolved_at,
            existing_incident[
                "incident_number"
            ]
        )
    )

    connection.commit()
    connection.close()

    existing_incident[
        "incident_status"
    ] = "RESOLVED"

    existing_incident[
        "resolved_at"
    ] = resolved_at

    return existing_incident, True


def get_all_incidents():
    """
    Return all incidents, newest first.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            incident_number,
            system_name,
            detected_status,
            response_time_ms,
            incident_status,
            detected_at,
            resolved_at
        FROM incidents
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    incidents = []

    for row in rows:

        incidents.append(
            {
                "incident_number": row[0],
                "system": row[1],
                "detected_status": row[2],
                "response_time_ms": row[3],
                "incident_status": row[4],
                "detected_at": row[5],
                "resolved_at": row[6]
            }
        )

    return incidents


initialize_database()

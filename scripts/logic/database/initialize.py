import mysql.connector
from scripts.logic.database.create_database import initialize_database, DB_NAME
from scripts.logic.database.initial_tables_fill import seed_initial_data


# Credentials of the dedicated app user — same as database_connection.py.
# This user has GRANT ALL PRIVILEGES, so it can create databases and tables
# without needing the root account.
_DB_HOST     = "127.0.0.1"
_DB_USER     = "budget_buddy_test"
_DB_PASSWORD = "strong_password_budget_buddies"


def initialize_all() -> bool:
    """Ensure the database, tables, and reference data all exist.

    Safe to call on every app startup:
      - CREATE DATABASE IF NOT EXISTS  → no-op if already there
      - CREATE TABLE IF NOT EXISTS     → no-op if already there
      - INSERT only if the row is absent → no-op if already seeded

    Returns:
        True  if initialization succeeded (or was already done).
        False if MySQL could not be reached (server down, wrong credentials).
    """
    try:
        # Step 1 — create the database and all tables.
        # The connection here intentionally has no `database=` argument
        # because the target database may not exist yet at this point.
        initialize_database(
            host=_DB_HOST,
            user=_DB_USER,
            password=_DB_PASSWORD,
        )

        # Step 2 — seed reference rows (OperationType, OperationCategory,
        # NotificationType). Uses INSERT only if the row is absent, so
        # running this multiple times is completely safe.
        connection = mysql.connector.connect(
            host=_DB_HOST,
            user=_DB_USER,
            password=_DB_PASSWORD,
            database=DB_NAME,
        )
        seed_initial_data(connection)
        connection.close()

        print("[OK] Database initialization complete")
        return True

    except mysql.connector.Error as err:
        print(f"[ERROR] Could not initialize database: {err}")
        return False
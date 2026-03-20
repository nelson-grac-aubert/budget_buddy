OPERATION_TYPES = [
    "deposit",
    "withdrawal",
    "transfer",
]

OPERATION_CATEGORIES = [
    "Espèces",
    "Chèque",
    "Loyer",
    "Courses",
    "Restaurants",
    "Abonnements",
    "Transport",
    "Santé",
    "Loisirs",
    "Salaire",
    "Revenus",
]

NOTIFICATION_TYPES = [
    "overdraft",
    "suspect activity",
    "big deposit",
    "big withdrawal",
]


def _insert_if_absent(cursor, table: str, column: str, value: str) -> None:
    """Insert a row into table only if no row with that column value exists."""
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = %s", (value,))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s)", (value,))


def seed_initial_data(connection) -> None:
    """Populate reference tables with their seed rows.

    Safe to call multiple times — rows are only inserted when absent.
    """
    cursor = connection.cursor()

    for label in OPERATION_TYPES:
        _insert_if_absent(cursor, "OperationType", "label", label)

    for label in OPERATION_CATEGORIES:
        _insert_if_absent(cursor, "OperationCategory", "label", label)

    for label in NOTIFICATION_TYPES:
        _insert_if_absent(cursor, "NotificationType", "label", label)

    connection.commit()
    cursor.close()
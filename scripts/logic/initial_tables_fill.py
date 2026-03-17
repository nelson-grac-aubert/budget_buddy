OPERATION_TYPES = [
    "deposit",
    "withdrawal",
    "transfer"
]

OPERATION_CATEGORIES = [
    "rent",
    "bills",
    "food",
    "car",
    "hobbies",
    "travels"
]

NOTIFICATION_TYPES = [
    "overdraft",
    "suspect activity",
    "big deposit",
    "big withdrawal"
]


def insert_if_not_exists(cursor, table, column, value):
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute(
            f"INSERT INTO {table} ({column}) VALUES (%s)",
            (value,)
        )
        print(f"[OK] Inserted into {table}: {value}")
    else:
        print(f"[SKIP] Already exists in {table}: {value}")


def seed_initial_data(connection):
    cursor = connection.cursor()

    for label in OPERATION_TYPES:
        insert_if_not_exists(cursor, "OperationType", "label", label)

    for label in OPERATION_CATEGORIES:
        insert_if_not_exists(cursor, "OperationCategory", "label", label)

    for label in NOTIFICATION_TYPES:
        insert_if_not_exists(cursor, "NotificationType", "label", label)

    connection.commit()
    cursor.close()
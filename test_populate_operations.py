import random
from datetime import datetime, timedelta
import mysql.connector

DB_NAME = "budget_buddy"

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="budget_buddy_test",
        password="strong_password_budget_buddies",
        database=DB_NAME
    )

# -----------------------------
# Helpers
# -----------------------------

def random_date(days_back=120):
    """Return a random datetime within the last X days."""
    delta = timedelta(days=random.randint(0, days_back))
    return datetime.now() - delta

def get_type_id(cursor, label):
    cursor.execute("SELECT id FROM OperationType WHERE label = %s", (label,))
    return cursor.fetchone()[0]

def get_category_id(cursor, label):
    cursor.execute("SELECT id FROM OperationCategory WHERE label = %s", (label,))
    return cursor.fetchone()[0]

def get_notification_type_id(cursor, label):
    cursor.execute("SELECT id FROM NotificationType WHERE label = %s", (label,))
    return cursor.fetchone()[0]

# -----------------------------
# Populate operations
# -----------------------------

def insert_operation(cursor, account_id, amount, description, type_label, category_label=None):
    type_id = get_type_id(cursor, type_label)
    category_id = get_category_id(cursor, category_label) if category_label else None

    query = """
        INSERT INTO Operation (account_id, destination_account_id, amount, description, type_id, date, category_id)
        VALUES (%s, NULL, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        account_id,
        amount,
        description,
        type_id,
        random_date(),
        category_id
    ))

def populate_operations_for_account(account_id=1):
    connection = get_connection()
    cursor = connection.cursor()

    operations = [
        ("deposit", 1200, "Salaire mensuel", "bills"),
        ("withdrawal", -45, "Courses au supermarché", "food"),
        ("withdrawal", -19, "Essence", "car"),
        ("withdrawal", -12, "Netflix", "hobbies"),
        ("withdrawal", -850, "Loyer", "rent"),
        ("deposit", 200, "Remboursement ami", "hobbies"),
        ("withdrawal", -65, "Restaurant", "food"),
        ("withdrawal", -300, "Billets de train", "travels"),
        ("deposit", 1500, "Prime exceptionnelle", "bills"),
    ]

    for type_label, amount, desc, category in operations:
        insert_operation(cursor, account_id, amount, desc, type_label, category)

    connection.commit()
    cursor.close()
    connection.close()

    print("[OK] Operations inserted")

# -----------------------------
# Populate notifications
# -----------------------------

def insert_notification(cursor, account_id, type_label, description):
    type_id = get_notification_type_id(cursor, type_label)

    query = """
        INSERT INTO Notification (account_id, type_id, description, created_at, is_read)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        account_id,
        type_id,
        description,
        random_date(),
        False
    ))

def populate_notifications_for_account(account_id=1):
    connection = get_connection()
    cursor = connection.cursor()

    notifications = [
        ("overdraft", "Votre compte est passé en négatif."),
        ("suspect activity", "Tentative de paiement refusée."),
        ("big deposit", "Un dépôt important a été détecté."),
    ]

    for type_label, desc in notifications:
        insert_notification(cursor, account_id, type_label, desc)

    connection.commit()
    cursor.close()
    connection.close()

    print("[OK] Notifications inserted")

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    populate_operations_for_account(1)
    populate_notifications_for_account(1)
    print("[OK] Test data population complete")
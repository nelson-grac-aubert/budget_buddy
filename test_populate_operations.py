import random
from datetime import datetime, timedelta
from scripts.logic.database_connection import get_connection

DB_NAME = "budget_buddy"

def get_type_id(cursor, label):
    """Return the OperationType.id matching the given label."""
    cursor.execute("SELECT id FROM OperationType WHERE label = %s", (label,))
    return cursor.fetchone()[0]

def get_category_id(cursor, label):
    """Return the OperationCategory.id matching the given label."""
    cursor.execute("SELECT id FROM OperationCategory WHERE label = %s", (label,))
    return cursor.fetchone()[0]

def get_notification_type_id(cursor, label):
    """Return the NotificationType.id matching the given label."""
    cursor.execute("SELECT id FROM NotificationType WHERE label = %s", (label,))
    return cursor.fetchone()[0]

def date_in_month(year, month, day=None):
    """Return a datetime for a specific year/month.

    If day is None, picks a random day between 1 and 28
    (safe for all months including February).
    """
    if day is None:
        day = random.randint(1, 28)
    return datetime(year, month, day)


def insert_operation(cursor, account_id, amount, description,
                     type_label, category_label, op_date):
    """Insert a single operation row with an explicit date.

    Args:
        cursor:         Active MySQL cursor.
        account_id:     Target account ID.
        amount:         Positive for deposits, negative for withdrawals.
        description:    Human-readable label for the operation.
        type_label:     Must match an existing OperationType.label.
        category_label: Must match an existing OperationCategory.label.
        op_date:        datetime object — sets the operation date precisely.
    """
    type_id     = get_type_id(cursor, type_label)
    category_id = get_category_id(cursor, category_label)

    cursor.execute("""
        INSERT INTO Operation
            (account_id, destination_account_id, amount, description,
             type_id, date, category_id)
        VALUES (%s, NULL, %s, %s, %s, %s, %s)
    """, (account_id, amount, description, type_id, op_date, category_id))

def populate_operations_for_account(account_id=1):
    """Insert realistic operations spread over 6 months.

    Each month has at least one salary deposit and several withdrawals,
    so the dashboard chart will always have enough data points to render
    the balance curve correctly.
    """
    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now()

    def month_offset(months_back):
        """Return (year, month) for N months before today."""
        month = today.month - months_back
        year  = today.year
        while month <= 0:
            month += 12
            year  -= 1
        return year, month
    
    operations = [

    (5, +800,  "Salaire partiel",          "deposit",    "Revenus"),
    (5, -400,  "Loyer",                    "withdrawal", "Loyer"),
    (5, -60,   "Courses",                  "withdrawal", "Courses"),
    (5, -15,   "Streaming",                "withdrawal", "Abonnements"),

    (4, +1200, "Salaire mensuel",          "deposit",    "Salaire"),
    (4, +500,  "Prime exceptionnelle",     "deposit",    "Revenus"),
    (4, -400,  "Loyer",                    "withdrawal", "Loyer"),
    (4, -80,   "Restaurant en famille",    "withdrawal", "Restaurants"),
    (4, -45,   "Essence",                  "withdrawal", "Transport"),
    (4, -19,   "Netflix",                  "withdrawal", "Abonnements"),

    (3, +1200, "Salaire mensuel",          "deposit",    "Salaire"),
    (3, -400,  "Loyer",                    "withdrawal", "Loyer"),
    (3, -300,  "Billets d'avion",          "withdrawal", "Loisirs"),
    (3, -120,  "Hotel",                    "withdrawal", "Loisirs"),
    (3, -90,   "Courses semaine",          "withdrawal", "Courses"),
    (3, -45,   "Essence",                  "withdrawal", "Transport"),

    (2, +1200, "Salaire mensuel",          "deposit",    "Salaire"),
    (2, +200,  "Remboursement ami",        "deposit",    "Revenus"),
    (2, -400,  "Loyer",                    "withdrawal", "Loyer"),
    (2, -65,   "Restaurant",               "withdrawal", "Restaurants"),
    (2, -55,   "Courses",                  "withdrawal", "Courses"),
    (2, -19,   "Spotify",                  "withdrawal", "Abonnements"),

    (1, +1200, "Salaire mensuel",          "deposit",    "Salaire"),
    (1, -400,  "Loyer",                    "withdrawal", "Loyer"),
    (1, -75,   "Courses du mois",          "withdrawal", "Courses"),
    (1, -45,   "Plein d'essence",          "withdrawal", "Transport"),
    (1, -12,   "Abonnement salle de sport","withdrawal", "Loisirs"),

    (0, +1200, "Salaire mensuel",          "deposit",    "Salaire"),
    (0, -400,  "Loyer",                    "withdrawal", "Loyer"),
    (0, -30,   "Courses express",          "withdrawal", "Courses")

    ]

    for months_back, amount, desc, type_label, category_label in operations:
        year, month = month_offset(months_back)
        op_date     = date_in_month(year, month)
        insert_operation(cursor, account_id, amount, desc,
                         type_label, category_label, op_date)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[OK] {len(operations)} operations inserted for account {account_id}")

    sync_account_balance(account_id)


def sync_account_balance(account_id):
    """Recompute Account.balance as the SUM of all operations for that account."""
    connection = get_connection()
    cursor = connection.cursor()

    # Sum all operation amounts for this account
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM Operation
        WHERE account_id = %s
    """, (account_id,))

    total = cursor.fetchone()[0]

    # Write the computed total back to Account.balance
    cursor.execute("""
        UPDATE Account
        SET balance = %s
        WHERE id = %s
    """, (total, account_id))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[OK] Account {account_id} balance synced to {total:.2f}")


def insert_notification(cursor, account_id, type_label, description, notif_date):
    """Insert a single notification row."""
    type_id = get_notification_type_id(cursor, type_label)

    cursor.execute("""
        INSERT INTO Notification
            (account_id, type_id, description, created_at, is_read)
        VALUES (%s, %s, %s, %s, %s)
    """, (account_id, type_id, description, notif_date, False))

def populate_notifications_for_account(account_id=1):
    """Insert a few sample notifications spread over recent months."""
    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now()

    notifications = [
        ("overdraft",        "Votre compte est passe en negatif.",    today - timedelta(days=90)),
        ("suspect activity", "Tentative de paiement refusee.",        today - timedelta(days=60)),
        ("big deposit",      "Un depot important a ete detecte.",     today - timedelta(days=30)),
    ]

    for type_label, desc, notif_date in notifications:
        insert_notification(cursor, account_id, type_label, desc, notif_date)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[OK] {len(notifications)} notifications inserted for account {account_id}")


if __name__ == "__main__":
    populate_operations_for_account(1)
    populate_notifications_for_account(1)
    print("[OK] Test data population complete")
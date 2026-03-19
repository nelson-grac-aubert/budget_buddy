from scripts.logic.database_connection import get_connection
from datetime import datetime

def get_user_fullname(user_id: int) -> str:
    """Return the full name of the user as 'Firstname Lastname'.

    Used by the dashboard greeting. Returns an empty string if the
    user is not found, so the label degrades gracefully.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT first_name, last_name FROM User WHERE id = %s",
        (user_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if not row:
        return ""
    return f"{row['first_name']} {row['last_name']}"


def get_account_balance(user_id: int) -> float:
    """Return the current balance of the user's account."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT balance
        FROM Account
        WHERE user_id = %s
    """, (user_id,))

    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row["balance"] if row else 0.0



    """Return the current balance of the user's account."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT balance
        FROM Account
        WHERE user_id = %s
    """, (user_id,))

    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row["balance"] if row else 0.0


def get_month_operations(user_id: int):
    """Return all operations for the current month."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT o.amount, o.date, oc.label AS category, ot.label AS type
        FROM Operation o
        JOIN Account a ON o.account_id = a.id
        JOIN OperationCategory oc ON o.category_id = oc.id
        JOIN OperationType ot ON o.type_id = ot.id
        WHERE a.user_id = %s
          AND MONTH(o.date) = MONTH(CURRENT_DATE())
          AND YEAR(o.date) = YEAR(CURRENT_DATE())
        ORDER BY o.date DESC
    """, (user_id,))

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return rows


def get_month_summary(user_id: int):
    """Return income and expenses for the current month."""
    ops = get_month_operations(user_id)

    income = sum(o["amount"] for o in ops if o["amount"] > 0)
    expenses = sum(abs(o["amount"]) for o in ops if o["amount"] < 0)

    return income, expenses


def get_balance_over_time(user_id: int) -> dict:
    """Return the cumulative balance after every operation, oldest to newest.

    One data point per operation — the x-axis label is the operation date
    (DD/MM), and the value is the running balance at that point in time.

    Example with 4 operations:
        Op 1  +1200  on 01/10  → balance: 1200   label: '01/10'
        Op 2   -400  on 05/10  → balance:  800   label: '05/10'
        Op 3   -850  on 18/10  → balance:  -50   label: '18/10'
        Op 4  +1500  on 02/11  → balance: 1450   label: '02/11'

    If two operations share the same date, the later one in insertion order
    wins — the label shows the final balance for that day.

    Returns:
        A dict { 'DD/MM': cumulative_balance } ordered oldest → newest.
        Returns an empty dict if the account has no operations.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT o.amount, o.date
        FROM Operation o
        JOIN Account a ON o.account_id = a.id
        WHERE a.user_id = %s
        ORDER BY o.date ASC
    """, (user_id,))

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Accumulate balance point by point
    cumulative = 0.0
    result     = {}
    for row in rows:
        cumulative      += float(row["amount"])
        label            = row["date"].strftime("%d/%m/%y")
        result[label]    = round(cumulative, 2)

    return result

# ---------------------------------------------------------------------------
# Aggregator — single entry point for the Dashboard widget
# ---------------------------------------------------------------------------

def get_dashboard_data(user_id: int) -> dict:
    """Fetch all data needed by the Dashboard in a single call.

    Calls the existing query functions and bundles their results into one
    dictionary so that app.py only needs one import and one call.

    Args:
        user_id: The ID of the currently logged-in user (from User table).

    Returns:
        A dict with keys:
            - "balance"         (float) : current account balance
            - "income"          (float) : total credits this month
            - "expenses"        (float) : total debits this month (positive)
            - "monthly_balance" (dict)  : { 'DD/MM': cumulative_balance, ... }
    """
    # Current account balance (already stored in Account.balance)
    balance = get_account_balance(user_id)

    # Income and expenses computed from this month's operations
    income, expenses = get_month_summary(user_id)

    # Balance curve: one point per operation, oldest to newest
    monthly_balance = get_balance_over_time(user_id)

    # Full name for the dashboard greeting ("Welcome Firstname Lastname")
    fullname = get_user_fullname(user_id)

    return {
        "balance":         balance,
        "income":          income,
        "expenses":        expenses,
        "monthly_balance": monthly_balance,
        "fullname":        fullname,
    }


def get_transactions_from_db(user_id: int):
    """Return all operations for the user's account in the format expected by the UI."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            o.date,
            o.amount,
            o.description,
            oc.label AS category,
            ot.label AS type
        FROM Operation o
        JOIN Account a ON o.account_id = a.id
        JOIN OperationCategory oc ON o.category_id = oc.id
        JOIN OperationType ot ON o.type_id = ot.id
        WHERE a.user_id = %s
        ORDER BY o.date DESC
    """

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # Adapt to the format expected by Cecilia's "relevé" window
    formatted = []
    for r in rows:
        formatted.append({
            "date": r["date"].strftime("%d/%m/%Y"),
            "description": r["description"],
            "categorie": r["category"],
            "type": "Crédit" if r["amount"] >= 0 else "Débit",
            "montant": float(r["amount"]),
        })

    return formatted
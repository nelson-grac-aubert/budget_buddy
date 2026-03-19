from scripts.logic.database_connection import get_connection
from datetime import datetime


def get_user_fullname(user_id: int) -> str:
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
    ops      = get_month_operations(user_id)
    income   = sum(o["amount"] for o in ops if o["amount"] > 0)
    expenses = sum(abs(o["amount"]) for o in ops if o["amount"] < 0)
    return income, expenses


def get_balance_over_time(user_id: int) -> dict:
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
    cumulative = 0.0
    result     = {}
    for row in rows:
        cumulative   += float(row["amount"])
        label         = row["date"].strftime("%d/%m/%y")
        result[label] = round(cumulative, 2)
    return result


def get_dashboard_data(user_id: int) -> dict:
    balance          = get_account_balance(user_id)
    income, expenses = get_month_summary(user_id)
    monthly_balance  = get_balance_over_time(user_id)
    fullname         = get_user_fullname(user_id)
    return {
        "balance":         balance,
        "income":          income,
        "expenses":        expenses,
        "monthly_balance": monthly_balance,
        "fullname":        fullname,
    }


def get_transactions_from_db(user_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
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
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        {
            "date":        r["date"].strftime("%d/%m/%Y"),
            "description": r["description"],
            "categorie":   r["category"],
            "type":        "Crédit" if r["amount"] >= 0 else "Débit",
            "montant":     float(r["amount"]),
        }
        for r in rows
    ]


# ── Admin ──

def get_all_accounts() -> list:
    """Retourne tous les comptes avec infos utilisateur et solde."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            u.id          AS user_id,
            a.id          AS account_id,
            u.first_name,
            u.last_name,
            u.email,
            a.balance
        FROM Account a
        JOIN User u ON a.user_id = u.id
        ORDER BY a.balance DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        {
            "user_id":    r["user_id"],
            "account_id": r["account_id"],
            "fullname":   f"{r['first_name']} {r['last_name']}",
            "email":      r["email"],
            "balance":    float(r["balance"]),
        }
        for r in rows
    ]
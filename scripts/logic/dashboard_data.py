from scripts.logic.database_connection import get_connection
from datetime import datetime

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


def get_monthly_balance(user_id: int):
    """Return a dict { 'Jan': 1234, 'Fév': 2345, ... } based on real operations."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            DATE_FORMAT(o.date, '%b') AS month,
            SUM(o.amount) AS total
        FROM Operation o
        JOIN Account a ON o.account_id = a.id
        WHERE a.user_id = %s
        GROUP BY YEAR(o.date), MONTH(o.date)
        ORDER BY YEAR(o.date), MONTH(o.date)
    """, (user_id,))

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return {row["month"]: row["total"] for row in rows}
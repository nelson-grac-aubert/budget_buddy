import mysql.connector

DB_NAME = "budget_buddy"


def get_connection():
    """Return a new MySQL connection to the budget_buddy database."""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="budget_buddy_test",
        password="strong_password_budget_buddies",
        database=DB_NAME
    )
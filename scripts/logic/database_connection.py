import mysql.connector

DB_NAME = "budget_buddy"

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="budget_buddy_test",
        password="strong_password_budget_buddies",
        database=DB_NAME
    )
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="budget_buddy_test",
        password="strong_password_budget_buddies"
    )
    print("Connected as:", conn.user, "@", conn.server_host)
except Exception as e:
    print("Error:", e)
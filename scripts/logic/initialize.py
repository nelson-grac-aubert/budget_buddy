from scripts.logic.create_database import initialize_database, DB_NAME
from scripts.logic.initial_tables_fill import seed_initial_data
import mysql.connector


def initialize_all(host="localhost", user="root", password=""):
    """
    Initialize the full database:
    - create database if needed
    - create all tables
    - seed initial data
    """
    # 1. Create DB + tables
    initialize_database(host=host, user=user, password=password)

    # 2. Connect to DB for seeding
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=DB_NAME
    )

    # 3. Seed initial data
    seed_initial_data(connection)

    # 4. Close connection
    connection.close()

    print("[OK] Full initialization complete")
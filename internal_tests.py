import mysql.connector

from scripts.logic.create_database import DB_NAME
from scripts.logic.initialize import initialize_all


def dump_database(host="127.0.0.1", user="budget_buddy_test", password="strong_password_budget_buddies"):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=DB_NAME
    )
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    print("\n=== FULL DATABASE DUMP ===\n")

    for (table_name,) in tables:
        print(f"\n--- {table_name} ---")

        cursor.execute(f"DESCRIBE {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        print("Columns:", columns)

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("(empty)")

    cursor.close()
    connection.close()
    print("\n=== END OF DUMP ===\n")


def create_john_doe(host="127.0.0.1", user="budget_buddy_test", password="strong_password_budget_buddies"):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=DB_NAME
    )
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO User (first_name, last_name, email, password_hash, type)
        VALUES (%s, %s, %s, %s, %s)
    """, ("John", "Doe", "john.doe@example.com", "hashed_password_john", "client"))

    connection.commit()
    cursor.close()
    connection.close()
    print("[OK] John Doe created")


def create_jane_doe(host="127.0.0.1", user="budget_buddy_test", password="strong_password_budget_buddies"):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=DB_NAME
    )
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO User (first_name, last_name, email, password_hash, type)
        VALUES (%s, %s, %s, %s, %s)
    """, ("Jane", "Doe", "jane.doe@example.com", "hashed_password_jane", "client"))

    connection.commit()
    cursor.close()
    connection.close()
    print("[OK] Jane Doe created")


def drop_database_completely(host="127.0.0.1", user="budget_buddy_test", password="strong_password_budget_buddies"):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    print(f"[OK] Database `{DB_NAME}` dropped completely")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    USER = "budget_buddy_test"
    PASSWORD = "strong_password_budget_buddies"

    # 1. Créer toute la DB (structure + seed)
    initialize_all(host=HOST, user=USER, password=PASSWORD)

    # 2. Créer John Doe
    # create_john_doe(host=HOST, user=USER, password=PASSWORD)

    # 3. Créer Jane Doe
    # create_jane_doe(host=HOST, user=USER, password=PASSWORD)

    # 4. Supprimer complètement la DB
    # drop_database_completely(host=HOST, user=USER, password=PASSWORD)

    # 5. Tout afficher pour tests
    dump_database(host=HOST, user=USER, password=PASSWORD)

    print("\nDone.")
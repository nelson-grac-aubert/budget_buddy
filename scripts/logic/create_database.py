import mysql.connector
from mysql.connector import errorcode

DB_NAME = "budget_buddy"

TABLES = {}

TABLES["User"] = (
    """
    CREATE TABLE IF NOT EXISTS User (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        type VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB;
    """
)

TABLES["Account"] = (
    """
    CREATE TABLE IF NOT EXISTS Account (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        balance FLOAT NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES User(id)
    ) ENGINE=InnoDB;
    """
)

TABLES["OperationType"] = (
    """
    CREATE TABLE IF NOT EXISTS OperationType (
        id INT AUTO_INCREMENT PRIMARY KEY,
        label VARCHAR(100) NOT NULL UNIQUE
    ) ENGINE=InnoDB;
    """
)

TABLES["OperationCategory"] = (
    """
    CREATE TABLE IF NOT EXISTS OperationCategory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        label VARCHAR(100) NOT NULL UNIQUE
    ) ENGINE=InnoDB;
    """
)

TABLES["Operation"] = (
    """
    CREATE TABLE IF NOT EXISTS Operation (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_id INT NOT NULL,
        destination_account_id INT,
        amount FLOAT NOT NULL,
        description VARCHAR(255),
        type_id INT NOT NULL,
        date DATETIME NOT NULL,
        category_id INT,
        FOREIGN KEY (account_id) REFERENCES Account(id),
        FOREIGN KEY (destination_account_id) REFERENCES Account(id),
        FOREIGN KEY (type_id) REFERENCES OperationType(id),
        FOREIGN KEY (category_id) REFERENCES OperationCategory(id)
    ) ENGINE=InnoDB;
    """
)

TABLES["NotificationType"] = (
    """
    CREATE TABLE IF NOT EXISTS NotificationType (
        id INT AUTO_INCREMENT PRIMARY KEY,
        label VARCHAR(100) NOT NULL UNIQUE
    ) ENGINE=InnoDB;
    """
)

TABLES["Notification"] = (
    """
    CREATE TABLE IF NOT EXISTS Notification (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_id INT NOT NULL,
        type_id INT NOT NULL,
        description VARCHAR(255),
        created_at DATETIME NOT NULL,
        is_read BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (account_id) REFERENCES Account(id),
        FOREIGN KEY (type_id) REFERENCES NotificationType(id)
    ) ENGINE=InnoDB;
    """
)


def create_database(cursor):
    """Create the database if it does not exist."""
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'"
        )
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        raise


def initialize_database(host="localhost", user="root", password=""):
    """
    Create the database and all tables.
    This function can be called from any external script.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        create_database(cursor)
        cursor.execute(f"USE {DB_NAME}")

        for table_name, ddl in TABLES.items():
            try:
                cursor.execute(ddl)
                print(f"Table `{table_name}` OK")
            except mysql.connector.Error as err:
                print(f"Error creating table {table_name}: {err}")

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        raise
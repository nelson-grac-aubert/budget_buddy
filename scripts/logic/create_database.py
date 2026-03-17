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
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)


def main():
    try:
        connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="noein210494"
        )
        cursor = connexion.cursor()

        # Create DB if needed
        create_database(cursor)

        # Select DB
        cursor.execute(f"USE {DB_NAME}")

        # Create tables
        for table_name, ddl in TABLES.items():
            try:
                cursor.execute(ddl)
                print(f"Table `{table_name}` OK")
            except mysql.connector.Error as err:
                print(f"Error creating table {table_name}: {err}")

        connexion.commit()
        cursor.close()
        connexion.close()

    except mysql.connector.Error as err:
        print(err)


if __name__ == "__main__":
    main()
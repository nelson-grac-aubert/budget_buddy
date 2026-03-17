#  la logique du menu d’acceuil, du login, du register
import re
import bcrypt
import mysql.connector
from mysql.connector import Error

DB_NAME = "budget_buddy"

def validate_password(password):
    """Check password strength."""
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{10,}$'
    return re.match(pattern, password)

def hash_password(password):
    """Return a bcrypt hashed password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(password, hashed):
    """Compare a plain password with a hashed one."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def validate_email(email):
    """Basic email format validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def get_connection():
    """Return a MySQL connection to the budget_buddy database."""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="budget_buddy_test",
        password="strong_password_budget_buddies",
        database=DB_NAME
    )

def insert_user(first_name, last_name, email, password_hash, user_type="client"):
    """Insert a new user into the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO User (first_name, last_name, email, password_hash, type)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (first_name, last_name, email, password_hash, user_type))
        connection.commit()

        cursor.close()
        connection.close()
        return True, "User registered successfully"

    except Error as err:
        if "Duplicate entry" in str(err):
            return False, "Email already exists"
        return False, f"MySQL error: {err}"

def get_user_by_email(email):
    """Retrieve a user by email."""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()
        return user

    except Error as err:
        print(f"MySQL error: {err}")
        return None

def handle_register(first_name, last_name, email, password):
    """Full registration process."""
    if not first_name or not last_name or not email or not password:
        return False, "All fields are required"

    if not validate_email(email):
        return False, "Invalid email format"

    if not validate_password(password):
        return False, (
            "Password must be at least 10 characters long and contain:\n"
            "- 1 uppercase letter\n"
            "- 1 lowercase letter\n"
            "- 1 digit\n"
            "- 1 special character"
        )

    hashed = hash_password(password)
    return insert_user(first_name, last_name, email, hashed)

def handle_login(email, password):
    """Full login process."""
    if not email or not password:
        return False, "Email and password are required"

    user = get_user_by_email(email)

    if user is None:
        return False, "User not found"

    if not check_password(password, user["password_hash"]):
        return False, "Incorrect password"

    return True, "Login successful"
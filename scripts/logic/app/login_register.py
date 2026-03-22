import re
import bcrypt
import mysql.connector
from mysql.connector import Error

DB_NAME = "budget_buddy"

def validate_password(password):
    # Regular expression (RegEx): a pattern used to validate or match strings
    """Check password strength."""
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[,@$!%*?&]).{10,}$'
    return re.match(pattern, password)

PEPPER = "my_super_secret_pepper"

def hash_password(password):
    """Return a bcrypt hashed password with pepper."""
    salted = (password + PEPPER).encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(salted, salt).decode()

def check_password(password, hashed):
    """Compare a plain password with a hashed one using pepper."""
    salted = (password + PEPPER).encode()
    return bcrypt.checkpw(salted, hashed.encode())

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
    """Insert a new user and automatically create an account."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insert user
        query = """
            INSERT INTO User (first_name, last_name, email, password_hash, type)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, password_hash, user_type))

        # Retrieve new user ID
        user_id = cursor.lastrowid

        # Create associated account
        cursor.execute(
            "INSERT INTO Account (user_id, balance) VALUES (%s, %s)",
            (user_id, 0)
        )

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

    # Hardcoded admin accoun
    if email == "admin" and password == "admin":
        return True, "Login Successful", 0, "admin"

    # regular user
    user = get_user_by_email(email)

    if user is None:
        return False, "User not found"

    if not check_password(password, user["password_hash"]):
        return False, "Incorrect password"

    return True, "Login Successful", user["id"], "client"


def update_password(user_id: int, new_password: str):
    """Hash and save a new password for the given user.

    Args:
        user_id:      ID of the user whose password is being changed.
        new_password: Plain-text new password (already validated by the UI).

    Returns:
        (True, "Password updated successfully") on success.
        (False, error_message) on failure.
    """
    if not validate_password(new_password):
        return False, "Password does not meet strength requirements"

    new_hash = hash_password(new_password)

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE User SET password_hash = %s WHERE id = %s",
            (new_hash, user_id)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return True, "Password updated successfully"

    except Error as err:
        return False, f"MySQL error: {err}"


def update_email(user_id: int, new_email: str):
    """Save a new email address for the given user.

    Args:
        user_id:   ID of the user whose email is being changed.
        new_email: New email address (validated for format before saving).

    Returns:
        (True, "Email updated successfully") on success.
        (False, error_message) on failure, including if the email is taken.
    """
    if not validate_email(new_email):
        return False, "Invalid email format"

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE User SET email = %s WHERE id = %s",
            (new_email, user_id)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return True, "Email updated successfully"

    except Error as err:
        if "Duplicate entry" in str(err):
            return False, "This email is already in use"
        return False, f"MySQL error: {err}"
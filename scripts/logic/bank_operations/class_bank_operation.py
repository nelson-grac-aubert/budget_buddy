import hashlib
from scripts.logic.database.database_connection import get_connection
from datetime import date

class BankOperation:
    def __init__(self, description, montant, categorie_id, account_id, destination_account_id=None):
        self.description = description
        self.montant = montant
        self.categorie_id = categorie_id
        self.date = date.today()
        self.account_id = account_id
        self.destination_account_id = destination_account_id
        self.reference = self.generate_reference()

    def generate_reference(self) -> str:
        """
        Generate a unique reference of about 10 characters based on operation data.
        Example : 'DEP-4F9A2C1B3'
        """
        # Create a base string using key operation attributes
        base = f"{self.description}{self.montant}{self.account_id}{self.date}"
        # Generate a SHA-1 hash and keep the first 7 characters
        hash_part = hashlib.sha1(base.encode()).hexdigest()[:7].upper()

        # Extract the first 3 alphanumeric characters from the description as a prefix
        prefix = ''.join(c for c in self.description.upper() if c.isalnum())[:3]
        # Combine prefix and hash to form the reference
        return f"{prefix}-{hash_part}"


    def save(self, operation_type_id: int):
        """Save the operation into the Operation table."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Operation
                    (account_id, destination_account_id, amount, description, type_id, date, category_id, reference)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.account_id,
                self.destination_account_id,
                self.montant,
                self.description,
                operation_type_id,
                self.date,
                self.categorie_id,
                self.reference
            ))

            conn.commit()

        except Exception as e:
            print("Erreur DB :", e)

        finally:
            conn.close()

    def update_balance(self, amount):
        """Update the account balance."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE account SET balance = balance + %s WHERE id=%s",
            (amount, self.account_id)
        )

        conn.commit()
        conn.close()

    def execute(self):
        """
        Method to be implemented in child classes.
        Defines how the operation should be executed.
        """
        raise NotImplementedError("Cette méthode doit être implémentée.")
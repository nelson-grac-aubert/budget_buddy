from scripts.logic.database_connection import get_connection
from datetime import date

class BankOperation:
    def __init__(self, description, montant, categorie_id, account_id, destination_account_id=None):
        self.description = description
        self.montant = montant
        self.categorie_id = categorie_id
        self.date = date.today()
        self.account_id = account_id
        self.destination_account_id = destination_account_id

    def save(self, operation_type_id: int):
        """Enregistre l'opération dans la table Operation."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Operation
                    (account_id, destination_account_id, amount, description, type_id, date, category_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                self.account_id,
                self.destination_account_id,
                self.montant,
                self.description,
                operation_type_id,
                self.date,
                self.categorie_id,
            ))

            conn.commit()

        except Exception as e:
            print("Erreur DB :", e)

        finally:
            conn.close()

    def execute(self):
        """Méthode à redéfinir dans les classes enfants."""
        raise NotImplementedError("Cette méthode doit être implémentée.")
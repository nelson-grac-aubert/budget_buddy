import hashlib
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
        self.reference = self.generate_reference()

    def generate_reference(self) -> str:
        """
        Génère une référence unique d'environ 10 caractères basée sur les données de l'opération.
        Exemple : 'DEP-4F9A2C1B3'
        """
        base = f"{self.description}{self.montant}{self.account_id}{self.date}"
        hash_part = hashlib.sha1(base.encode()).hexdigest()[:7].upper()

        # 3 premières lettres de la description (nettoyées)
        prefix = ''.join(c for c in self.description.upper() if c.isalnum())[:3]

        return f"{prefix}-{hash_part}"


    def save(self, operation_type_id: int):
        """Enregistre l'opération dans la table Operation."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Operation
                    (account_id, destination_account_id, amount, description, type_id, date, category_id, reference)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
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
        """ Update la somme sur le compte en banque """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE account SET balance = balance + %s WHERE id=%s",
            (amount, self.account_id)
        )

        conn.commit()
        conn.close()

    def execute(self):
        """Méthode à redéfinir dans les classes enfants."""
        raise NotImplementedError("Cette méthode doit être implémentée.")
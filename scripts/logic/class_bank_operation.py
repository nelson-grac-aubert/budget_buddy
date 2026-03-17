#class BankOperation : 
# models/transaction
from create_database import main
from datetime import date
import uuid

from create_database import main
from datetime import date
import uuid

class BankOperation:
    def __init__(self, description, montant, categorie, sender, receiver=None):
        self.reference = str(uuid.uuid4())[:8]
        self.description = description
        self.montant = montant
        self.categorie = categorie
        self.date = date.today()
        self.sender = sender
        self.receiver = receiver

    def save(self, operation_type):
        try:
            conn = main()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Operation
                (reference, description, montant, type, categorie, date, sender_id, receiver_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.reference,
                self.description,
                self.montant,
                operation_type,
                self.categorie,
                self.date,
                self.sender.id,
                self.receiver.id if self.receiver else None
            ))

            conn.commit()

        except Exception as e:
            print("Erreur DB :", e)

        finally:
            conn.close()

    def execute(self):
        """Méthode à redéfinir dans les classes enfants"""
        raise NotImplementedError("Cette méthode doit être implémentée.")
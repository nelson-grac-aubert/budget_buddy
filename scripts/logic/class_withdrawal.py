from scripts.logic.class_bank_operation import BankOperation

class Withdrawal(BankOperation):
    def execute(self):
        """Plus tard : vérifier le solde, mettre à jour Account.balance, etc."""
        # Pour l'instant, on se contente d'enregistrer l'opération
        self.save(operation_type_id=2)  # 2 = 'withdrawal' dans OperationType
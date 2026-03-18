from scripts.logic.class_bank_operation import BankOperation

class Withdrawal(BankOperation):
    def execute(self):
        """Plus tard : vérifier le solde, mettre à jour Account.balance, etc."""
        self.save(operation_type_id=2)  # 2 = 'withdrawal' dans OperationType
        self.update_balance(self.montant)
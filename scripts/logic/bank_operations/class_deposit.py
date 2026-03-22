from scripts.logic.bank_operations.class_bank_operation import BankOperation

class Deposit(BankOperation):
    def execute(self):
        self.save(operation_type_id=1)  # 1 = "deposit" in OperationType
        self.update_balance(self.montant)

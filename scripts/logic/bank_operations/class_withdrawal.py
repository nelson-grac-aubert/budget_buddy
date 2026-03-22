from scripts.logic.bank_operations.class_bank_operation import BankOperation

class Withdrawal(BankOperation):
    def execute(self):
        #  Implement balance validation and update Account.balance accordingly
        self.save(operation_type_id=2)  # 2 = 'withdrawal' in OperationType
        self.update_balance(self.montant)
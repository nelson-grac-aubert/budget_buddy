from scripts.logic.class_bank_operation import BankOperation

class Deposit(BankOperation):
    def execute(self):
        self.sender.update_balance(self.montant)
        self.save("depot")
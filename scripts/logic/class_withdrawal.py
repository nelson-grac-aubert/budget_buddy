from scripts.logic.class_bank_operation import BankOperation

class Withdrawal(BankOperation):
    def execute(self):
        if self.sender.balance < self.montant:
            raise Exception("Solde insuffisant")

        self.sender.update_balance(-self.montant)
        self.save("retrait")

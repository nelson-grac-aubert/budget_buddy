from scripts.logic.class_bank_operation import BankOperation

class Transfer(BankOperation):
    def execute(self):
        if not self.receiver:
            raise Exception("Receiver requis pour un transfert")

        if self.sender.balance < self.montant:
            raise Exception("Solde insuffisant")

        self.sender.update_balance(-self.montant)
        self.receiver.update_balance(self.montant)

        self.save("transfert")

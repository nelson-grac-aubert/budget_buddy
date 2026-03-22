from scripts.logic.bank_operations.class_bank_operation import BankOperation


class Transfer:
    """Record a transfer between two accounts.
Creates two Operation entries with type_id = 3 (transfer):
  - a negative outgoing transaction from the source account
  - a positive incoming transaction to the destination account"""

    def __init__(self, description, montant, categorie_id,
                 source_account_id, destination_account_id):
        self.description            = description
        self.montant                = montant
        self.categorie_id           = categorie_id
        self.source_account_id      = source_account_id
        self.destination_account_id = destination_account_id

    def execute(self):
        # Debit operation on the source account (negative amount)
        sortie = BankOperation(
            description=self.description,
            montant=-self.montant,
            categorie_id=self.categorie_id,
            account_id=self.source_account_id,
            destination_account_id=self.destination_account_id,
        )
        sortie.save(operation_type_id=3)   # 3 = 'transfer'
        sortie.update_balance(-self.montant)

        # Credit operation on the destination account (positive amount)
        entree = BankOperation(
            description=self.description,
            montant=self.montant,
            categorie_id=self.categorie_id,
            account_id=self.destination_account_id,
            destination_account_id=self.source_account_id,
        )
        entree.save(operation_type_id=3)   # 3 = 'transfer'
        entree.update_balance(self.montant)
from scripts.logic.bank_operations.class_bank_operation import BankOperation


class Transfer:
    """Enregistre un virement entre deux comptes.
    Crée deux lignes Operation avec type_id=3 (transfer) :
      - une sortie négative sur le compte source
      - une entrée positive sur le compte destination
    """

    def __init__(self, description, montant, categorie_id,
                 source_account_id, destination_account_id):
        self.description            = description
        self.montant                = montant
        self.categorie_id           = categorie_id
        self.source_account_id      = source_account_id
        self.destination_account_id = destination_account_id

    def execute(self):
        # Opération de débit sur le compte source (montant négatif)
        sortie = BankOperation(
            description=self.description,
            montant=-self.montant,
            categorie_id=self.categorie_id,
            account_id=self.source_account_id,
            destination_account_id=self.destination_account_id,
        )
        sortie.save(operation_type_id=3)   # 3 = 'transfer'
        sortie.update_balance(-self.montant)

        # Opération de crédit sur le compte destination (montant positif)
        entree = BankOperation(
            description=self.description,
            montant=self.montant,
            categorie_id=self.categorie_id,
            account_id=self.destination_account_id,
            destination_account_id=self.source_account_id,
        )
        entree.save(operation_type_id=3)   # 3 = 'transfer'
        entree.update_balance(self.montant)
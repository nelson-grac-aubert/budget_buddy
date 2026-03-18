from create_database import main
from logic.login_register import hash_password, check_password, validate_password

class User:
    def __init__(self, id, nom, prenom, email, account_id, user_type):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.account_id = account_id
        self.type = user_type

    @staticmethod
    def register(nom, prenom, email, password, user_type="client"):
        if not validate_password(password):
            return "Mot de passe invalide"

        hashed = hash_password(password)
        conn = main()
        cursor = conn.cursor()

        # Création d’un compte bancaire (table accounts)
        cursor.execute("INSERT INTO accounts (balance) VALUES (0)")
        account_id = cursor.lastrowid

        # Création de l’utilisateur lié au compte
        cursor.execute(
            "INSERT INTO users (nom, prenom, email, password, account_id, type) VALUES (%s,%s,%s,%s,%s,%s)",
            (nom, prenom, email, hashed.decode(), account_id, user_type)
        )

        conn.commit()
        conn.close()
        return "Utilisateur créé"

    @staticmethod
    def login(email, password):
        conn = main()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        data = cursor.fetchone()

        conn.close()

        if data and check_password(password, data["password"]):
            return User(
                data["id"],
                data["nom"],
                data["prenom"],
                data["email"],
                data["account_id"],
                data["type"]
            )
        return None

    def get_balance(self):
        conn = main()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT balance FROM accounts WHERE id=%s",
            (self.account_id,)
        )
        result = cursor.fetchone()

        conn.close()
        return result["balance"] if result else 0

    